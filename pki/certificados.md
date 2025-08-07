

## Gerando uma CA

### O que é uma CA?

Uma **Certificate Authority (CA)** é uma entidade que emite e gerencia certificados digitais. Em ambientes de desenvolvimento ou corporativos, você pode criar sua própria CA para emitir certificados internos.

### Estrutura de Diretórios

Primeiro, vamos criar uma estrutura organizada:

```bash
# Criar estrutura de diretórios
mkdir -p ca/{private,certs,newcerts,crl}
mkdir -p ca/intermediate/{private,certs,newcerts,crl}
chmod 700 ca/private
chmod 700 ca/intermediate/private

# Criar arquivos necessários
touch ca/index.txt
touch ca/serial
echo "01" > ca/serial

touch ca/intermediate/index.txt
touch ca/intermediate/serial
echo "01" > ca/intermediate/serial
```

### Configuração do OpenSSL para CA

Crie um arquivo `openssl-ca.cnf` para a CA raiz:

```ini
[ca]
default_ca = CA_default

[CA_default]
# Diretórios
dir               = ./ca
certs             = $dir/certs
crl_dir           = $dir/crl
new_certs_dir     = $dir/newcerts
database          = $dir/index.txt
serial            = $dir/serial
RANDFILE          = $dir/private/.rand

# Chave privada da CA
private_key       = $dir/private/ca.key
certificate       = $dir/certs/ca.crt

# Configurações de assinatura
crlnumber         = $dir/crlnumber
crl               = $dir/crl/ca.crl
crl_extensions    = crl_ext
default_crl_days  = 30

# Extensões padrão
default_md        = sha256
name_opt         = ca_default
cert_opt         = ca_default
default_days     = 365
preserve         = no
policy           = policy_strict

[policy_strict]
countryName             = match
stateOrProvinceName     = match
organizationName        = match
organizationalUnitName  = optional
commonName              = supplied
emailAddress            = optional

[policy_loose]
countryName             = optional
stateOrProvinceName     = optional
localityName            = optional
organizationName        = optional
organizationalUnitName  = optional
commonName              = supplied
emailAddress            = optional

[req]
default_bits        = 4096
distinguished_name  = req_distinguished_name
string_mask         = utf8only
default_md          = sha256
x509_extensions     = v3_ca

[req_distinguished_name]
countryName                     = Country Name (2 letter code)
stateOrProvinceName             = State or Province Name
localityName                    = Locality Name
0.organizationName              = Organization Name
organizationalUnitName          = Organizational Unit Name
commonName                      = Common Name
emailAddress                    = Email Address

[ v3_ca ]
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true
keyUsage = critical, digitalSignature, cRLSign, keyCertSign

[ server_cert ]
basicConstraints = CA:FALSE
nsCertType = server
nsComment = "OpenSSL Generated Server Certificate"
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer:always
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth

[ usr_cert ]
basicConstraints = CA:FALSE
nsCertType = client, email
nsComment = "OpenSSL Generated Client Certificate"
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer:always
keyUsage = critical, nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = clientAuth, emailProtection

[ server_client_cert ]
basicConstraints = CA:FALSE
nsCertType = server, client, email
nsComment = "OpenSSL Generated Server/Client Certificate"
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer:always
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth, clientAuth

[ crl_ext ]
authorityKeyIdentifier=keyid:always
```

### Passo 1: Criando a CA Raiz

```bash
# 1. Gerar chave privada da CA raiz
openssl genrsa -aes256 -out ca/private/ca.key 4096

# 2. Criar certificado da CA raiz
openssl req -config openssl-ca.cnf \
    -key ca/private/ca.key \
    -new -x509 -days 7300 -sha256 -extensions v3_ca \
    -out ca/certs/ca.crt

# 3. Verificar o certificado da CA
openssl x509 -in ca/certs/ca.crt -text -noout
```

### Passo 2: Criando CA Intermediária

Crie um arquivo `openssl-intermediate.cnf`:

```ini
[ca]
default_ca = CA_default

[CA_default]
dir               = ./ca/intermediate
certs             = $dir/certs
crl_dir           = $dir/crl
new_certs_dir     = $dir/newcerts
database          = $dir/index.txt
serial            = $dir/serial
RANDFILE          = $dir/private/.rand

private_key       = $dir/private/intermediate.key
certificate       = $dir/certs/intermediate.crt

crlnumber         = $dir/crlnumber
crl               = $dir/crl/intermediate.crl
crl_extensions    = crl_ext
default_crl_days  = 30

default_md        = sha256
name_opt         = ca_default
cert_opt         = ca_default
default_days     = 365
preserve         = no
policy           = policy_loose

[policy_strict]
countryName             = match
stateOrProvinceName     = match
organizationName        = match
organizationalUnitName  = optional
commonName              = supplied
emailAddress            = optional

[policy_loose]
countryName             = optional
stateOrProvinceName     = optional
localityName            = optional
organizationName        = optional
organizationalUnitName  = optional
commonName              = supplied
emailAddress            = optional

[req]
default_bits        = 4096
distinguished_name  = req_distinguished_name
string_mask         = utf8only
default_md          = sha256
x509_extensions     = v3_intermediate_ca

[req_distinguished_name]
countryName                     = Country Name (2 letter code)
stateOrProvinceName             = State or Province Name
localityName                    = Locality Name
0.organizationName              = Organization Name
organizationalUnitName          = Organizational Unit Name
commonName                      = Common Name
emailAddress                    = Email Address

[v3_intermediate_ca]
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true, pathlen:0
keyUsage = critical, digitalSignature, cRLSign, keyCertSign

[server_cert]
basicConstraints = CA:FALSE
nsCertType = server
nsComment = "OpenSSL Generated Server Certificate"
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer:always
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth

[usr_cert]
basicConstraints = CA:FALSE
nsCertType = client, email
nsComment = "OpenSSL Generated Client Certificate"
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer:always
keyUsage = critical, nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = clientAuth, emailProtection

[crl_ext]
authorityKeyIdentifier=keyid:always
```

Agora crie a CA intermediária:

```bash
# 1. Gerar chave privada da CA intermediária
openssl genrsa -aes256 -out ca/intermediate/private/intermediate.key 4096

# 2. Criar CSR da CA intermediária
openssl req -config openssl-intermediate.cnf -new -sha256 \
    -key ca/intermediate/private/intermediate.key \
    -out ca/intermediate/certs/intermediate.csr

# 3. Assinar com a CA raiz
openssl ca -config openssl-ca.cnf -extensions v3_intermediate_ca \
    -days 3650 -notext -md sha256 \
    -in ca/intermediate/certs/intermediate.csr \
    -out ca/intermediate/certs/intermediate.crt

# 4. Verificar o certificado intermediário
openssl x509 -in ca/intermediate/certs/intermediate.crt -text -noout
```

### Passo 3: Assinando Certificados com a CA

#### Assinando com CA Raiz

```bash
# Assinar certificado de servidor
openssl ca -config openssl-ca.cnf \
    -extensions server_cert -days 375 -notext -md sha256 \
    -in request.csr -out server.crt

# Assinar certificado de cliente
openssl ca -config openssl-ca.cnf \
    -extensions usr_cert -days 375 -notext -md sha256 \
    -in request.csr -out client.crt
```

#### Assinando com CA Intermediária

```bash
# Assinar certificado de servidor
openssl ca -config openssl-intermediate.cnf \
    -extensions server_cert -days 375 -notext -md sha256 \
    -in request.csr -out server.crt

# Assinar certificado de cliente
openssl ca -config openssl-intermediate.cnf \
    -extensions usr_cert -days 375 -notext -md sha256 \
    -in request.csr -out client.crt
```

### Passo 4: Criando Cadeia de Certificados

```bash
# Cadeia completa (CA raiz + intermediária + certificado)
cat ca/certs/ca.crt ca/intermediate/certs/intermediate.crt > ca-chain.crt

# Cadeia intermediária (intermediária + certificado)
cat ca/intermediate/certs/intermediate.crt > intermediate-chain.crt
```

### Comandos Úteis para CA

```bash
# Listar certificados emitidos
openssl ca -config openssl-ca.cnf -list

# Revogar certificado
openssl ca -config openssl-ca.cnf -revoke certificado.crt

# Gerar CRL (Certificate Revocation List)
openssl ca -config openssl-ca.cnf -gencrl -out ca/crl/ca.crl

# Verificar CRL
openssl crl -in ca/crl/ca.crl -text -noout

# Verificar certificado
openssl verify -CAfile ca/certs/ca.crt certificado.crt

# Verificar cadeia completa
openssl verify -CAfile ca-chain.crt certificado.crt
```

### Estrutura Final

```
ca/
├── private/
│   ├── ca.key
│   └── .rand
├── certs/
│   ├── ca.crt
│   └── intermediate.crt
├── intermediate/
│   ├── private/
│   │   └── intermediate.key
│   ├── certs/
│   │   ├── intermediate.csr
│   │   └── intermediate.crt
│   ├── newcerts/
│   ├── crl/
│   ├── index.txt
│   └── serial
├── newcerts/
├── crl/
├── index.txt
└── serial
```


