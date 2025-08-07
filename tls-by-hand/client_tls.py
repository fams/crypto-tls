
import socket
import struct
import os
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Hash import HMAC, SHA1
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
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

def build_record(content_type, version, payload):
    return struct.pack('!BHH', content_type, int.from_bytes(version, 'big'), len(payload)) + payload

def recv_exact(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise ConnectionError("Conexão encerrada")
        data += more
    return data

def read_tls_record(sock):
    header = recv_exact(sock, 5)
    content_type, version, length = struct.unpack('!BHH', header)
    return content_type, recv_exact(sock, length)

def run_client():
    sock = socket.create_connection(("localhost", 4433))

    client_random = get_random_bytes(32)
    session_id = SESSION_ID_EMPTY
    # Usar cipher suites compatíveis com TLS 1.0
    cipher_suites = struct.pack('!H', len(CIPHER_SUITES_CLIENT) * 2) + b''.join(CIPHER_SUITES_CLIENT)
    compression_methods = struct.pack('!B', 1) + COMPRESSION_NULL

    body = TLS_VERSION_1_0 + client_random + session_id + cipher_suites + compression_methods
    client_hello = HANDSHAKE_TYPE_CLIENT_HELLO + struct.pack('!I', len(body))[1:] + body
    sock.send(build_record(HANDSHAKE, TLS_VERSION_1_0, client_hello))

    _, sh_rec = read_tls_record(sock)
    sh_body = sh_rec[4:]  # remove header da handshake
    server_random = sh_body[2:34]

    _, server_cert_record = read_tls_record(sock)
    server_cert_data = server_cert_record[7:]  # Skip handshake headers
    try:
        server_cert = x509.load_der_x509_certificate(server_cert_data, default_backend())
    except Exception as e:
        print("[!] Erro ao carregar o certificado:")
        print("    Tipo de dado recebido:", type(server_cert_data))
        print("    Tamanho:", len(server_cert_data))
        print("    Primeiros bytes (hex):", server_cert_data[:30].hex())
        raise e
    server_pubkey = server_cert.public_key()
    server_rsa_pubkey = RSA.import_key(
        server_pubkey.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

    _, _ = read_tls_record(sock)

    pre_master_secret = TLS_VERSION_1_0 + get_random_bytes(46)
    cipher_rsa = PKCS1_v1_5.new(server_rsa_pubkey)
    encrypted_pms = cipher_rsa.encrypt(pre_master_secret)
    ckx = HANDSHAKE_TYPE_CLIENT_KEY_EXCHANGE + struct.pack('!I', len(encrypted_pms))[1:] + encrypted_pms
    sock.send(build_record(HANDSHAKE, TLS_VERSION_1_0, ckx))

    sock.send(build_record(CHANGE_CIPHER_SPEC, TLS_VERSION_1_0, CCS_BYTE))
    sock.send(build_record(HANDSHAKE, TLS_VERSION_1_0, b'finalizado12345678'))

    seed = client_random + server_random
    master_secret = tls_prf(pre_master_secret, b"master secret", seed, 48)
    key_seed = server_random + client_random  # (inverso da ordem do master_secret)
    key_block = tls_prf(master_secret, b"key expansion", key_seed, 104)
    server_write_key = key_block[56:72]  # 16 bytes
    server_write_iv = key_block[88:104]  # 16 bytes

    _, ciphertext = read_tls_record(sock)
    cipher = AES.new(server_write_key, AES.MODE_CBC, server_write_iv)
    plaintext = unpad(cipher.decrypt(ciphertext), 16)
    print("[+] Mensagem recebida do servidor:", plaintext.decode())

    sock.close()

if __name__ == "__main__":
    run_client()
