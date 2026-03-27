# Lab 07

Criptografia Asimétrica

## Diffie Hellman

### Programa `dh.py`

Exemplo de utilização:

```bash
$ python dh.py
[Bob]   K = 415350919b6ee6ca26513db3d5012f1addbca7c45bee7209bcfb2b44fb8118c3cc3f20170ce3fd9cbded23bdd7164ce52a373bcf5ecfd189841e8c0700bc42da
[Alice] K = 415350919b6ee6ca26513db3d5012f1addbca7c45bee7209bcfb2b44fb8118c3cc3f20170ce3fd9cbded23bdd7164ce52a373bcf5ecfd189841e8c0700bc42da
```

### Programa `dh_aes_gcm.py`

Exemplo de utilização:

```bash
$ python dh_aes_gcm.py
[Alice] K       = 38d5713b1a1b27284cf7ca5788706f9421aaeb2fd3f4dfc22a1dc7bc5d3c085b14127d39a7e2618ef934c549a82ddf2fd600752fa2db91706ea9edba3f4bb944
[Bob]   K       = 38d5713b1a1b27284cf7ca5788706f9421aaeb2fd3f4dfc22a1dc7bc5d3c085b14127d39a7e2618ef934c549a82ddf2fd600752fa2db91706ea9edba3f4bb944
[Alice] aes_key = 6811ea6eccbaf1f33c7faa8ac79d3d887822da22def3a30c56c864fb8439666b
[Bob]   aes_key = 6811ea6eccbaf1f33c7faa8ac79d3d887822da22def3a30c56c864fb8439666b
[Alice] Sent encrypted message (nonce=392e70e17c9593b0b6c72c01)
[Bob]   Decrypted message: Hello Bob, this message is confidential!
```

### Questão 01

O protocolo tal como está não garante PFS. PFS significa que, se o segredo K for comprometido no futuro, as mensagens trocadas anteriormente continuam seguras. Isso exige que as chaves DH sejam **efémeras** - geradas de novo em cada sessão e descartadas após uso. O problema está na KDF: se o atacante obtiver K, pode re-derivar `aes_key = HKDF(K)` e desencriptar **todas** as mensagens que usaram essa chave, porque a mesma `aes_key` foi reutilizada em todas elas. Para garantir PFS, seria necessário gerar um novo par de chaves DH por mensagem (ou por sessão), de forma a que cada troca produza um K diferente e independente. Assim, comprometer um K apenas expõe as mensagens dessa sessão.

## Certificados

### Questão 02

As chaves públicas estão armazenadas nos **certificados X.509** (ficheiros `.crt`). O certificado da CA (`CA.crt`) é self-signed - a CA assina o seu próprio certificado com a sua chave privada. Os certificados de Alice (`Alice.crt`) e Bob (`Bob.crt`) são assinados pela CA, ou seja, a CA usa a sua chave privada para atestar que a chave pública contida em cada certificado pertence de facto a esse participante. O processo de criação passa primeiro por um CSR (_Certificate Signing Request_), gerado com a chave privada do utilizador, por exemplo `Alice.key`. O CSR contém a chave pública correspondente e é enviado à CA, que o assina e emite o certificado final. Quem quiser verificar a chave pública de Alice abre `Alice.crt`, confirma que a assinatura da CA é válida usando `CA.crt`, e só então confia na chave pública que lá está.

## DH Autenticado

### Programa `sts_aes_gcm.py`

Exemplo de utilização:

```shell
$ python sts_aes_gcm.py
[Alice] Sent DH public key (g^x)
[Bob]   Received Alice's DH public key (g^x)
[Bob]   Sent DH public key, signature and certificate
[Alice] Bob's certificate is valid
[Alice] Bob's signature is valid
[Alice] Sent signature and certificate
[Alice] K       = 8cd6a0941e5879b9f8efed70784482372c2d0c9ee98e7190aa2b05610a80d654c6a04c1458a45b62d75e91b8869a9af741c3af0451b715fb3b16100f3cf99e2c
[Alice] aes_key = 6ae810be4e60c7c7b3f2739854ab442374c6c2be8340f6fb8dcc32ea601556a6
[Bob]   Alice's certificate is valid
[Alice] Sent encrypted message (nonce=5809a7dfd530e467841441d1)
[Bob]   Alice's signature is valid
[Bob]   K       = 8cd6a0941e5879b9f8efed70784482372c2d0c9ee98e7190aa2b05610a80d654c6a04c1458a45b62d75e91b8869a9af741c3af0451b715fb3b16100f3cf99e2c
[Bob]   aes_key = 6ae810be4e60c7c7b3f2739854ab442374c6c2be8340f6fb8dcc32ea601556a6
[Bob]   Decrypted message: Hello Bob, this is authenticated and confidential!
```

### Questão 03

O protocolo fica vulnerável a ataques _Man-in-the-Middle_. A verificação da assinatura do Bob prova que alguém com a chave privada correspondente ao certificado apresentado assinou `(g^y, g^x)`. Mas sem verificar o certificado contra a CA, Alice não tem forma de saber a quem pertence essa chave privada. Um atacante pode gerar o seu próprio par de chaves RSA, criar um certificado falso com o nome "Bob", e assinar com a sua chave privada, a verificação da assinatura passa na mesma, porque a assinatura é consistente com o certificado apresentado. O ataque funciona da seguinte forma: Mallory (atacante) interceta `g^x` de Alice, substitui por `g^m` para Bob, e faz o mesmo no sentido inverso. Em cada lado apresenta um certificado falso não verificado. Alice verifica a assinatura de Mallory com o certificado falso de Mallory e aceita. O resultado é que Alice estabelece K com Mallory, e Bob estabelece um K diferente também com Mallory, sem nenhum dos dois se aperceber. A verificação do certificado é o que quebra este ataque, garante que a chave pública no certificado foi atestada pela CA, ligando-a a uma identidade real. A assinatura sozinha apenas prova posse da chave privada, não a identidade de quem a possui.
