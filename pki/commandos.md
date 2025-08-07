# Comandos OpenSSL - TLS, Certificados e Truststore

## 🔗 Conectar em Servidor TLS

### Conexão básica
```bash
# Conectar e mostrar informações do certificado
openssl s_client -connect example.com:443

# Conectar com SNI (Server Name Indication)
openssl s_client -connect example.com:443 -servername example.com

# Conectar e mostrar apenas o certificado
openssl s_client -connect example.com:443 -showcerts

# Conectar com verificação de hostname
openssl s_client -connect example.com:443 -verify_return_error
```

### Conexão com truststore customizado
```bash
# Usar CA bundle customizado
openssl s_client -connect example.com:443 -CAfile /path/to/ca-bundle.pem

# Usar diretório de CAs
openssl s_client -connect example.com:443 -CApath /path/to/ca/directory

# Ignorar verificação (não recomendado para produção)
openssl s_client -connect example.com:443 -verify_return_error -verify 0
```

## 🔐 Verificar Chave Pública vs Privada

### Verificar correspondência RSA
```bash
# Extrair chave pública da privada
openssl rsa -in private_key.pem -pubout -out public_key.pem

# Verificar se correspondem (mesmo hash)
openssl rsa -in private_key.pem -pubout | openssl sha256
openssl rsa -pubin -in public_key.pem -pubout | openssl sha256
# Se os hashes forem iguais, as chaves correspondem
```

### Verificar correspondência ECDSA
```bash
# Extrair chave pública ECDSA
openssl ec -in private_key.pem -pubout -out public_key.pem

# Verificar correspondência
openssl ec -in private_key.pem -pubout | openssl sha256
openssl ec -pubin -in public_key.pem -pubout | openssl sha256
```

## 🔍 Verificar Certificado contra Truststore

### Verificar com CA bundle
```bash
# Verificar certificado contra CA bundle
openssl verify -CAfile ca-bundle.pem certificate.pem

# Verificar cadeia completa
openssl verify -CAfile ca-bundle.pem -untrusted intermediate.pem certificate.pem

# Verificar com diretório de CAs
openssl verify -CApath /etc/ssl/certs certificate.pem
```

### Verificar certificado de servidor
```bash
# Verificar certificado de servidor remoto
openssl s_client -connect example.com:443 -CAfile ca-bundle.pem -verify_return_error
```

## 🌐 Conectar com Truststore Customizado

### Usar CA bundle específico
```bash
# Conectar usando truststore customizado
openssl s_client -connect example.com:443 -CAfile my-ca-bundle.pem

# Conectar com múltiplos CAs
openssl s_client -connect example.com:443 -CAfile ca1.pem -CAfile ca2.pem

# Conectar com diretório de CAs
openssl s_client -connect example.com:443 -CApath /path/to/ca/directory
```

### Verificar certificado específico
```bash
# Verificar certificado de servidor específico
openssl s_client -connect example.com:443 -servername example.com -CAfile ca-bundle.pem
```

## 🖥️ Servir TLS

### Servidor TLS básico
```bash
# Servir com certificado e chave
openssl s_server -cert server_cert.pem -key server_key.pem -port 8443

# Servir com verificação de cliente
openssl s_server -cert server_cert.pem -key server_key.pem -port 8443 -verify 1

# Servir com CA para verificar clientes
openssl s_server -cert server_cert.pem -key server_key.pem -port 8443 -CAfile ca.pem -verify 2
```

### Servidor TLS com cadeia
```bash
# Servir com cadeia completa
openssl s_server -cert server_chain.pem -key server_key.pem -port 8443

# Servir com certificado e CA separados
openssl s_server -cert server_cert.pem -key server_key.pem -CAfile ca.pem -port 8443
```

## 📋 Mostrar Certificados de Servidor

### Informações básicas
```bash
# Mostrar certificado do servidor
openssl s_client -connect example.com:443 -showcerts

# Mostrar apenas o certificado (sem conexão)
openssl s_client -connect example.com:443 -showcerts < /dev/null

# Mostrar cadeia completa
openssl s_client -connect example.com:443 -showcerts -servername example.com
```

### Salvar certificados
```bash
# Salvar certificado do servidor
openssl s_client -connect example.com:443 -showcerts < /dev/null | openssl x509 -outform PEM > server_cert.pem

# Salvar cadeia completa
openssl s_client -connect example.com:443 -showcerts < /dev/null > chain.pem
```

## 📄 Mostrar Dados de Certificado

### Informações básicas
```bash
# Mostrar dados do certificado
openssl x509 -in certificate.pem -text -noout

# Mostrar apenas subject e issuer
openssl x509 -in certificate.pem -subject -issuer -noout

# Mostrar datas de validade
openssl x509 -in certificate.pem -dates -noout

# Mostrar extensões
openssl x509 -in certificate.pem -extensions -noout
```

### Informações específicas
```bash
# Mostrar subject
openssl x509 -in certificate.pem -subject -noout

# Mostrar issuer
openssl x509 -in certificate.pem -issuer -noout

# Mostrar serial number
openssl x509 -in certificate.pem -serial -noout

# Mostrar fingerprint
openssl x509 -in certificate.pem -fingerprint -noout
```

## 🔄 Converter Formatos

### PEM para DER
```bash
# Certificado PEM para DER
openssl x509 -in certificate.pem -outform DER -out certificate.der

# Chave privada PEM para DER
openssl rsa -in private_key.pem -outform DER -out private_key.der

# Chave pública PEM para DER
openssl rsa -pubin -in public_key.pem -outform DER -out public_key.der
```

### DER para PEM
```bash
# Certificado DER para PEM
openssl x509 -inform DER -in certificate.der -out certificate.pem

# Chave privada DER para PEM
openssl rsa -inform DER -in private_key.der -out private_key.pem

# Chave pública DER para PEM
openssl rsa -pubin -inform DER -in public_key.der -out public_key.pem
```

### Outros formatos
```bash
# PEM para PKCS#8
openssl pkcs8 -topk8 -in private_key.pem -out private_key_pkcs8.pem

# PKCS#8 para PEM
openssl pkcs8 -in private_key_pkcs8.pem -out private_key.pem

# PEM para PKCS#12
openssl pkcs12 -export -in certificate.pem -inkey private_key.pem -out certificate.p12
```

## 📦 Formato PKCS#7

### Criar PKCS#7
```bash
# Criar PKCS#7 com certificado
openssl crl2pkcs7 -nocrl -certfile certificate.pem -out certificate.p7b

# Criar PKCS#7 com cadeia
openssl crl2pkcs7 -nocrl -certfile server_cert.pem -certfile ca_cert.pem -out chain.p7b

# Criar PKCS#7 com certificado e CRL
openssl crl2pkcs7 -certfile certificate.pem -crlfile crl.pem -out cert_with_crl.p7b
```

### Verificar PKCS#7
```bash
# Mostrar conteúdo PKCS#7
openssl pkcs7 -in certificate.p7b -print_certs -noout

# Extrair certificados de PKCS#7
openssl pkcs7 -in certificate.p7b -print_certs -out certificates.pem

# Verificar PKCS#7
openssl pkcs7 -in certificate.p7b -verify -noout
```

### Converter PKCS#7
```bash
# PKCS#7 para PEM
openssl pkcs7 -in certificate.p7b -print_certs -out certificate.pem

# PKCS#7 para DER
openssl pkcs7 -in certificate.p7b -outform DER -out certificate.p7c
```

## 🛠️ Comandos Úteis

### Verificar conectividade
```bash
# Teste rápido de conectividade
echo | openssl s_client -connect example.com:443 -servername example.com

# Teste com timeout
timeout 10 openssl s_client -connect example.com:443
```

### Debug TLS
```bash
# Debug detalhado da conexão
openssl s_client -connect example.com:443 -debug

# Mostrar cipher suites suportados
openssl s_client -connect example.com:443 -cipher ALL

# Testar cipher específico
openssl s_client -connect example.com:443 -cipher ECDHE-RSA-AES256-GCM-SHA384
```

### Verificar truststore
```bash
# Listar certificados em CA bundle
openssl crl2pkcs7 -nocrl -certfile ca-bundle.pem | openssl pkcs7 -print_certs -noout

# Verificar certificado específico no truststore
openssl verify -CAfile ca-bundle.pem -verbose certificate.pem
```
