
# Constantes simbólicas para TLS 1.0
TLS_VERSION_1_0 = b'\x03\x01'
HANDSHAKE = 22
CHANGE_CIPHER_SPEC = 20
APPLICATION_DATA = 23
COMPRESSION_NULL = b'\x00'

# TLS Handshake Message Types
HANDSHAKE_TYPE_CLIENT_HELLO = b'\x01'
HANDSHAKE_TYPE_SERVER_HELLO = b'\x02'
HANDSHAKE_TYPE_CERTIFICATE = b'\x0b'
HANDSHAKE_TYPE_SERVER_HELLO_DONE = b'\x0e\x00\x00\x00'
HANDSHAKE_TYPE_CLIENT_KEY_EXCHANGE = b'\x10'
CIPHER_TLS_DHE_RSA_WITH_AES_128_CBC_SHA = b'\x00\x33'
# Session-ID
SESSION_ID_EMPTY      = b'\x00'            # length-0 = sem resumption
# Cipher-suites (RFC 5246 Appendix A)
CIPHER_TLS_RSA_WITH_AES_128_CBC_SHA = b'\x00\x2f'  # TLS 1.0/1.1
CIPHER_TLS_RSA_WITH_3DES_EDE_CBC_SHA = b'\x00\x0A'  # TLS 1.0/1.1
# Compression methods (RFC 2246 §6.2.2)
CCS_BYTE                          = b'\x01'   # 0x01 = ChangeCipherSpec fragment
# Compression methods (RFC 2246 §6.2.2)
COMPRESSION_METHODS  = [COMPRESSION_NULL]
CIPHER_SUITES_CLIENT = [
    CIPHER_TLS_RSA_WITH_AES_128_CBC_SHA,      # preferencial
    CIPHER_TLS_RSA_WITH_3DES_EDE_CBC_SHA      # fallback
]
