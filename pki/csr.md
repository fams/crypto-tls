# Aprendendo a usar o OpenSSL

## Mini Tutorial: Certificate Signing Request (CSR)

### O que é um CSR?

Um **Certificate Signing Request (CSR)** é um arquivo que contém informações sobre você ou sua organização que serão incluídas no certificado digital. O CSR é enviado para uma Autoridade Certificadora (CA) que irá assinar e emitir o certificado.

### Passo 1: Criando a Chave Privada

Antes de criar o CSR, você precisa gerar uma chave privada. A chave privada deve ser mantida segura e nunca compartilhada.

#### Opção 1: Chave RSA (Recomendada)
```bash
# Gerar chave privada RSA de 2048 bits
openssl genrsa -out private.key 2048

# Para maior segurança, use 4096 bits
openssl genrsa -out private.key 4096
```

#### Opção 2: Chave com senha (Mais segura)
```bash
# Gerar chave privada com senha
openssl genrsa -aes256 -out private.key 2048
```

#### Opção 3: Chave ECDSA (Mais moderna)
```bash
# Gerar chave privada ECDSA usando curva P-256
openssl ecparam -genkey -name prime256v1 -out private.key
```

### Passo 2: Criando o CSR

Agora vamos criar o CSR usando a chave privada gerada:

#### Método Interativo
```bash
# Criar CSR de forma interativa
openssl req -new -key private.key -out request.csr
```

Durante o processo interativo, você será solicitado a fornecer:
- **Country Name (2 letter code)**: BR (para Brasil)
- **State or Province Name**: Seu estado
- **Locality Name**: Sua cidade
- **Organization Name**: Nome da sua organização
- **Organizational Unit Name**: Departamento (opcional)
- **Common Name**: Nome do domínio (ex: www.exemplo.com)
- **Email Address**: Seu email
- **Challenge password**: Deixe em branco (Enter)
- **Optional Company Name**: Deixe em branco (Enter)

#### Método com arquivo de configuração
Crie um arquivo `openssl.conf`:
```ini
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = BR
ST = Sao Paulo
L = Sao Paulo
O = Minha Empresa
OU = TI
CN = www.exemplo.com
emailAddress = admin@exemplo.com

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = www.exemplo.com
DNS.2 = exemplo.com
```

Então execute:
```bash
openssl req -new -key private.key -out request.csr -config openssl.conf
```

### Passo 3: Verificando o CSR

Sempre verifique o conteúdo do CSR antes de enviá-lo:

```bash
# Ver o conteúdo do CSR
openssl req -in request.csr -text -noout

# Ver apenas as informações do subject
openssl req -in request.csr -noout -subject
```

### Passo 4: Enviando o CSR

O arquivo `request.csr` deve ser enviado para a Autoridade Certificadora (CA) de sua escolha. A CA irá:

1. Verificar suas informações
2. Assinar o certificado
3. Retornar o certificado assinado

### Exemplo Completo

Aqui está um exemplo completo de criação de CSR:

```bash
# 1. Criar diretório para o projeto
mkdir meu-certificado
cd meu-certificado

# 2. Gerar chave privada
openssl genrsa -out private.key 2048

# 3. Criar CSR
openssl req -new -key private.key -out request.csr

# 4. Verificar o CSR
openssl req -in request.csr -text -noout

# 5. Verificar a chave privada
openssl rsa -in private.key -check
```

### Extensões e Usage

As extensões X.509 definem como o certificado pode ser usado e quais são suas capacidades. Vamos entender as principais extensões:

#### Extensões Básicas

**1. KeyUsage (KU)**
Define para que a chave pode ser usada:
```bash
# Para certificados de servidor web
keyUsage = digitalSignature, keyEncipherment

# Para certificados de CA
keyUsage = keyCertSign, cRLSign

# Para certificados de cliente
keyUsage = digitalSignature, keyAgreement
```

**2. ExtendedKeyUsage (EKU)**
Define o propósito específico do certificado:
```bash
# Para servidor web
extendedKeyUsage = serverAuth

# Para cliente
extendedKeyUsage = clientAuth

# Para assinatura de código
extendedKeyUsage = codeSigning

# Para email seguro
extendedKeyUsage = emailProtection
```

#### Extensões Avançadas

**1. SubjectAltName (SAN)**
Permite múltiplos nomes de domínio no mesmo certificado:
```ini
[alt_names]
DNS.1 = www.exemplo.com
DNS.2 = exemplo.com
DNS.3 = api.exemplo.com
IP.1 = 192.168.1.100
```

**2. BasicConstraints**
Define se o certificado pode ser usado como CA:
```bash
# Para certificado final (não CA)
basicConstraints = CA:FALSE

# Para certificado CA
basicConstraints = CA:TRUE, pathlen:0
```

#### Exemplo de Configuração Completa

Aqui está um exemplo de arquivo de configuração com extensões apropriadas:

```ini
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = BR
ST = Sao Paulo
L = Sao Paulo
O = Minha Empresa
OU = TI
CN = www.exemplo.com
emailAddress = admin@exemplo.com

[v3_req]
# Uso da chave
keyUsage = digitalSignature, keyEncipherment, dataEncipherment

# Propósito específico
extendedKeyUsage = serverAuth, clientAuth

# Nomes alternativos
subjectAltName = @alt_names

# Restrições básicas
basicConstraints = CA:FALSE

# Política de certificado
certificatePolicies = @pol_section

[alt_names]
DNS.1 = www.exemplo.com
DNS.2 = exemplo.com
DNS.3 = api.exemplo.com
DNS.4 = *.exemplo.com

[pol_section]
policyIdentifier = 1.3.6.1.4.1.12345.1
CPS.1 = https://www.exemplo.com/cps
```

#### Tipos de Usage Comuns

**Para Servidor Web:**
```bash
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
```

**Para Cliente:**
```bash
keyUsage = digitalSignature, keyAgreement
extendedKeyUsage = clientAuth
```

**Para Assinatura de Código:**
```bash
keyUsage = digitalSignature
extendedKeyUsage = codeSigning
```

**Para Email:**
```bash
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = emailProtection
```

#### Verificando Extensões

Para verificar as extensões de um certificado:
```bash
# Ver todas as extensões
openssl x509 -in certificado.crt -text -noout

# Ver apenas extensões específicas
openssl x509 -in certificado.crt -text -noout | grep -A 10 "X509v3 extensions"

# Verificar SAN
openssl x509 -in certificado.crt -text -noout | grep -A 5 "Subject Alternative Name"
```

#### Dicas sobre Extensões

1. **SAN é obrigatório**: Certificados modernos devem usar SubjectAltName
2. **Wildcards**: Use `*.exemplo.com` para subdomínios
3. **IPs**: Inclua IPs se necessário para desenvolvimento

### Comandos Úteis

```bash
# Verificar se a chave privada é válida
openssl rsa -in private.key -check

# Verificar o tamanho da chave
openssl rsa -in private.key -text -noout | grep "Private-Key"

# Converter CSR para formato PEM (se necessário)
openssl req -in request.csr -outform PEM -out request.pem

# Verificar assinatura do CSR
openssl req -in request.csr -verify
```

## Análise ASN.1 e Codificação Binária do CSR

### Estrutura ASN.1 do CSR

Um CSR (Certificate Signing Request) segue a estrutura ASN.1 definida no RFC 2986. Vamos analisar sua codificação binária:

### Visualizando a Estrutura ASN.1

```bash
# Ver a estrutura ASN.1 completa do CSR
openssl asn1parse -in request.csr -i

# Ver com mais detalhes (mostra offsets)
openssl asn1parse -in request.csr -i -dump

```

## Mostrando OIDs dos Campos do CSR

### O que são OIDs?

**OID (Object Identifier)** é um identificador único que define o tipo de cada campo em estruturas ASN.1. No contexto de certificados e CSRs, os OIDs identificam campos como país, organização, etc.

### Visualizando OIDs com OpenSSL

#### 1. Ver OIDs no Subject
```bash
# Ver OIDs do Subject com detalhes
openssl req -in request.csr -noout -subject -nameopt RFC2253,show_type

# Ver OIDs com formato mais detalhado
openssl req -in request.csr -noout -subject -nameopt RFC2253,show_type,utf8

# Ver apenas os OIDs numéricos
openssl req -in request.csr -noout -subject -nameopt RFC2253,show_type | grep -o "OID.[0-9.]*"
```

#### 2. Ver OIDs em Formato Legível
```bash
# Ver OIDs com nomes legíveis
openssl req -in request.csr -noout -subject -nameopt RFC2253,show_type,utf8,esc_2253

# Ver OIDs com escape de caracteres especiais
openssl req -in request.csr -noout -subject -nameopt RFC2253,show_type,esc_2253,esc_msb
```

#### 3. Analisar OIDs com ASN.1
```bash
# Ver estrutura ASN.1 com OIDs
openssl asn1parse -in request.csr -i -dump

# Ver apenas a seção do Subject com OIDs
openssl asn1parse -in request.csr -strparse 4 -i -dump

# Ver OIDs em formato hexadecimal
openssl asn1parse -in request.csr -strparse 4 -hexdump
```

### OIDs Comuns em CSRs

#### OIDs do Subject
```bash
# Lista de OIDs comuns
echo "OIDs comuns em certificados:"
echo "2.5.4.6  = Country (C)"
echo "2.5.4.8  = State or Province (ST)"
echo "2.5.4.7  = Locality (L)"
echo "2.5.4.10 = Organization (O)"
echo "2.5.4.11 = Organizational Unit (OU)"
echo "2.5.4.3  = Common Name (CN)"
echo "1.2.840.113549.1.9.1 = Email Address"
```

#### OIDs de Algoritmos
```bash
# Ver algoritmo de assinatura
openssl req -in request.csr -noout -text | grep "Signature Algorithm"

# Ver OID do algoritmo de assinatura
openssl asn1parse -in request.csr -i | grep "OBJECT"
```

### Script para Análise Completa de OIDs

```bash
#!/bin/bash
# Script para mostrar todos os OIDs de um CSR

CSR_FILE="$1"

if [ -z "$CSR_FILE" ]; then
    echo "Uso: $0 <arquivo.csr>"
    exit 1
fi

echo "=== Análise de OIDs do CSR: $CSR_FILE ==="

# 1. Verificar se o arquivo existe
if [ ! -f "$CSR_FILE" ]; then
    echo "Erro: Arquivo $CSR_FILE não encontrado"
    exit 1
fi

# 2. Verificar se é um CSR válido
if ! openssl req -in "$CSR_FILE" -verify > /dev/null 2>&1; then
    echo "ERRO: CSR inválido ou corrompido"
    exit 1
fi

echo "✓ CSR válido"

# 3. Mostrar Subject com OIDs
echo -e "\n=== Subject com OIDs ==="
openssl req -in "$CSR_FILE" -noout -subject -nameopt RFC2253,show_type

# 4. Extrair OIDs do Subject
echo -e "\n=== OIDs Extraídos do Subject ==="
openssl req -in "$CSR_FILE" -noout -subject -nameopt RFC2253,show_type | \
    grep -o "OID.[0-9.]*" | sort | uniq

# 5. Ver algoritmo de assinatura
echo -e "\n=== Algoritmo de Assinatura ==="
openssl req -in "$CSR_FILE" -noout -text | grep "Signature Algorithm"

# 6. Ver OIDs na estrutura ASN.1
echo -e "\n=== OIDs na Estrutura ASN.1 ==="
openssl asn1parse -in "$CSR_FILE" -i | grep "OBJECT"

# 7. Ver extensões com OIDs
echo -e "\n=== Extensões com OIDs ==="
openssl req -in "$CSR_FILE" -noout -text | grep -A 20 "X509v3 extensions" | grep "OBJECT"

echo -e "\n=== Análise de OIDs Concluída ==="
```

### Comandos Avançados para OIDs

#### 1. Mapear OIDs para Nomes
```bash
# Criar mapeamento de OIDs comuns
cat > oid_mapping.txt << 'EOF'
2.5.4.6=Country
2.5.4.8=State
2.5.4.7=Locality
2.5.4.10=Organization
2.5.4.11=OrganizationalUnit
2.5.4.3=CommonName
1.2.840.113549.1.9.1=EmailAddress
1.2.840.113549.1.1.11=sha256WithRSAEncryption
1.2.840.113549.1.1.1=rsaEncryption
EOF

# Usar o mapeamento
while IFS='=' read -r oid name; do
    echo "OID $oid = $name"
done < oid_mapping.txt
```

#### 2. Ver OIDs em Extensões
```bash
# Ver OIDs das extensões
openssl req -in request.csr -noout -text | grep -A 30 "X509v3 extensions" | grep "OBJECT"

# Ver OIDs específicos de extensões
openssl req -in request.csr -noout -text | grep -E "(keyUsage|extendedKeyUsage|subjectAltName)" -A 5
```

#### 3. Analisar OIDs com Ferramentas Externas
```bash
# Usar oid-info.com para decodificar OIDs
# Exemplo: https://oid-info.com/get/2.5.4.6

# Verificar OID com OpenSSL
echo "2.5.4.6" | openssl asn1parse -genstr OID
```

### Exemplo de Saída com OIDs

```bash
# Exemplo de saída típica
$ openssl req -in request.csr -noout -subject -nameopt RFC2253,show_type
subject=OID.2.5.4.6=BR, OID.2.5.4.8=Sao Paulo, OID.2.5.4.7=Sao Paulo, OID.2.5.4.10=Minha Empresa, OID.2.5.4.11=TI, OID.2.5.4.3=www.exemplo.com, OID.1.2.840.113549.1.9.1=admin@exemplo.com
```

### Dicas para Trabalhar com OIDs

1. **Formato**: OIDs são representados como números separados por pontos
2. **Padrão**: OIDs começam com 2.5.4 para campos do Subject
3. **Algoritmos**: OIDs de algoritmos começam com 1.2.840.113549
4. **Extensões**: Cada extensão tem seu próprio OID
5. **Verificação**: Sempre verifique se o OID está correto
6. **Documentação**: Consulte RFCs para OIDs específicos

### Comandos Úteis para Debug de OIDs

```bash
# Verificar se um OID específico está presente
openssl req -in request.csr -noout -subject -nameopt RFC2253,show_type | grep "2.5.4.6"

# Comparar OIDs entre dois CSRs
diff <(openssl req -in csr1.csr -noout -subject -nameopt RFC2253,show_type) \
     <(openssl req -in csr2.csr -noout -subject -nameopt RFC2253,show_type)

# Ver OIDs em formato DER
openssl req -in request.csr -outform DER | openssl asn1parse -i -dump
```
