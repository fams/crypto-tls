#!/usr/bin/env python3
"""
Servidor HTTP simples com TLS usando http.server
"""

import http.server
import socketserver
import ssl
import argparse
from pathlib import Path

class SimpleHTTPServer:
    def __init__(self, cert_file, key_file, port=8443):
        self.cert_file = cert_file
        self.key_file = key_file
        self.port = port
        
    def create_ssl_context(self):
        """Cria contexto SSL"""
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(self.cert_file, self.key_file)
        return context
    
    def run(self):
        """Executa o servidor"""
        # Cria o servidor HTTP
        handler = http.server.SimpleHTTPRequestHandler
        
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            # Envolve com SSL
            httpd.socket = self.create_ssl_context().wrap_socket(
                httpd.socket, 
                server_side=True
            )
            
            print(f"[+] Servidor HTTPS rodando em localhost:{self.port}")
            print(f"[+] Certificado: {self.cert_file}")
            print(f"[+] Chave: {self.key_file}")
            print("[+] Pressione Ctrl+C para parar")
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n[!] Servidor encerrado")

def main():
    parser = argparse.ArgumentParser(description='Servidor HTTPS simples')
    parser.add_argument('--cert', required=True, help='Arquivo do certificado')
    parser.add_argument('--key', required=True, help='Arquivo da chave privada')
    parser.add_argument('--port', type=int, default=8443, help='Porta (padrão: 8443)')
    
    args = parser.parse_args()
    
    # Verifica arquivos
    if not Path(args.cert).exists():
        print(f"[!] Certificado não encontrado: {args.cert}")
        return 1
    
    if not Path(args.key).exists():
        print(f"[!] Chave não encontrada: {args.key}")
        return 1
    
    # Executa servidor
    server = SimpleHTTPServer(args.cert, args.key, args.port)
    server.run()
    
    return 0

if __name__ == "__main__":
    exit(main()) 