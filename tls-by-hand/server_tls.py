
import socket
import struct
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA1
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import padding
from constants import *


def tls_prf(secret, label, seed, size):
    result = b''
    a = label + seed
    hmac = HMAC.new(secret, a, SHA1)
    a = hmac.digest()
    while len(result) < size:
        hmac = HMAC.new(secret, a + label + seed, SHA1)
        result += hmac.digest()
        hmac = HMAC.new(secret, a, SHA1)
        a = hmac.digest()
    return result[:size]

def recv_exact(conn, length):
    data = b''
    while len(data) < length:
        more = conn.recv(length - len(data))
        if not more:
            raise ConnectionError("Conexão encerrada")
        data += more
    return data

def build_record(content_type, version, payload):
    return struct.pack("!BHH", content_type, int.from_bytes(version, "big"), len(payload)) + payload

def read_tls_record(conn):
    header = recv_exact(conn, 5)
    content_type, version, length = struct.unpack("!BHH", header)
    return content_type, recv_exact(conn, length)

def choose_cipher(client_hello_data: bytes) -> bytes:
    SUPPORTED_CIPHER_SUITES = [CIPHER_TLS_RSA_WITH_AES_128_CBC_SHA]
    session_id_len = client_hello_data[34]
    offset = 35 + session_id_len
    cipher_list_len = struct.unpack('!H', client_hello_data[offset:offset+2])[0]
    offset += 2
    client_ciphers = [client_hello_data[i:i+2] for i in range(offset, offset + cipher_list_len, 2)]
    for cipher in client_ciphers:
        if cipher in SUPPORTED_CIPHER_SUITES:
            return cipher
    return None

def run_server():
    with open("../server_key.pem", "rb") as f:
        server_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

    with open("../server_cert.pem", "rb") as f:
        server_certificate_der = x509.load_pem_x509_certificate(f.read(), default_backend())
        server_certificate_der = server_certificate_der.public_bytes(serialization.Encoding.DER)

    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", 4433))
    sock.listen(1)
    print("[*] Aguardando conexão TLS...")

    conn, addr = sock.accept()
    print(f"[+] Conexão recebida de {addr}")

    _, handshake_record = read_tls_record(conn)

    # Extrair apenas o corpo da handshake
    client_hello = handshake_record[4:]
    client_random = client_hello[2:34]  # 32b após cabeçalhos
    chosen_cipher = choose_cipher(client_hello)
    if not chosen_cipher:
        print("[!] Nenhuma cifra compatível encontrada. Encerrando.")
        conn.close()
        return

    server_random = get_random_bytes(32)
    session_id = SESSION_ID_EMPTY
    cipher_suite = chosen_cipher
    compression = COMPRESSION_NULL
    server_hello_body = TLS_VERSION_1_0 + server_random + session_id + cipher_suite + compression
    server_hello = HANDSHAKE_TYPE_SERVER_HELLO + struct.pack("!I", len(server_hello_body))[1:] + server_hello_body
    conn.send(build_record(HANDSHAKE, TLS_VERSION_1_0, server_hello))

    cert_body = struct.pack("!I", len(server_certificate_der))[1:] + server_certificate_der
    certificate = HANDSHAKE_TYPE_CERTIFICATE + struct.pack("!I", len(cert_body))[1:] + cert_body
    conn.send(build_record(HANDSHAKE, TLS_VERSION_1_0, certificate))

    conn.send(build_record(HANDSHAKE, TLS_VERSION_1_0, HANDSHAKE_TYPE_SERVER_HELLO_DONE))

    _, ckx = read_tls_record(conn)
    encrypted_pms = ckx[4:]
    pre_master_secret = server_key.decrypt(encrypted_pms, padding.PKCS1v15())

    seed = client_random + server_random
    master_secret = tls_prf(pre_master_secret, b"master secret", seed, 48)
    # seed correto para key_block = ServerRandom || ClientRandom   (RFC 2246 §6.3)
    key_seed = server_random + client_random
    key_block = tls_prf(master_secret, b"key expansion", key_seed, 104)
    server_write_key = key_block[56:72]  # 16 bytes
    server_write_iv = key_block[88:104]  # 16 bytes

    _, _ = read_tls_record(conn)  # ChangeCipherSpec
    _, _ = read_tls_record(conn)  # Finished

    plaintext = b"mensagem segura do servidor"
    cipher = AES.new(server_write_key, AES.MODE_CBC, server_write_iv[:16])
    padded = pad(plaintext, 16)
    ciphertext = cipher.encrypt(padded)
    conn.send(build_record(APPLICATION_DATA, TLS_VERSION_1_0, ciphertext))
    print("[+] Mensagem criptografada enviada")

    conn.close()

if __name__ == "__main__":
    run_server()
