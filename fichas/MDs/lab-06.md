# Semana 7

## MACs

Analogamente a cifras simétricas, que garantem *confidencialidade*, é possível construir Message Authenticated Codes (MACs) que, dada uma chave secreta simétrica, garantem *integridade*.

### PROG: `mac_sha256.py`

Vamos começar por explorar a construção mais simples de um MAC a partir de uma função de hash, denominada **prefix-MAC**: $MAC(k,m) = H(k \parallel m)$.

Defina o programa `mac_sha256.py` que calcula o MAC de um ficheiro usando a função de hash [`SHA256`](https://cryptography.io/en/latest/hazmat/primitives/cryptographic-hashes/). O programa receba como argumentos:
 * o tipo de operação a realizar: `setup`, `mac` ou `ver`
   - `setup <fkey>` cria ficheiro contendo uma chave apropriada para o MAC `SHA256` (com nome `<fkey>`)
   - `mac <fich> <fkey>` calcula o MAC do ficheiro passado como argumento `<fich>`, usando a chave lida do ficheiro `<fkey>`. O MAC resultante deverá ser gravado em `<fich>.mac` (i.e. adiciona a extensão `.mac` ao nome do ficheiro de mensagem).
   - `ver <fich> <fkey>` verifica o MAC de `<fich>` contido em `<fich>.mac`, usando a chave lida do ficheiro `<fkey>`. Imprime um booleano.

> [!NOTE]
> Como o nome indica, a função de hash `SHA256` utiliza chaves de `32` bytes, logo `32 * 8 = 256` bits.

### PROG: `mac_sha256_attack.py`

Recorde, como apresentado na aula teórica, a construção **prefix-MAC**, quando utilizada com funções de hash da família `SHA-2` (que utiliza a construção de Merkle–Damgård), é vulnerável a length extension attacks: um atacante, sem conhecer a chave, consegue forjar um novo MAC válido para uma extensão da mensagem original.
Construa o programa `mac_sha256_attack.py` que demonstra um ataque deste tipo. O programa deve receber os argumentos `<fich> <ext>`, sendo que `<fich>` e `<fich>.mac` são respetivamente os nomes dos ficheiros contendo a mensagem e MAC originais, e `<ext>` é o texto que se pretende adicionar à mensagem. A mensagem e o MAC estendidos devem ser gravados em `<fich>.ext` e `<fich>.ext.mac` respetivamente. Teste o sucesso do seu ataque, verificando o MAC para a chave original.

> [!NOTE]
> Infelizmente, a biblioteca `cryptography` não permite aceder ao estado interno da função de hash, e a solução mais recorrente é programar diretamente sobre os bindings `C` da biblioteca [`openssl`](https://docs.openssl.org/3.2/man3/SHA256_Init/#synopsis). Para simplificar e realizar o ataque de forma quase completamente automática, sugere-se que recorra à biblioteca [`hashpumpy`](https://github.com/2H-K/hashpumpy_changed).

> [!TIP]
> O `SHA256` processa a mensagem em blocos de 512 bits. Um ataque de extensão consiste em acrescentar um ou mais novos blocos à mensagem, sendo necessário para isso recalcular o padding da mensagem original $m$, e calcular um novo MAC para a mensagem estendida $m \parallel padding \parallel ext$. O padding é acrescentado automaticamente pela biblioteca `hashpumpy`.

### QUESTÃO: Q1

Considere que a mensagem é o URL `http://www.super-secret.com/manage?id=1001&role=user&perm=read`, e que o ataque consiste em estender a mensagem com o texto `&admin=true`. Qual o padding acrescentado pelo programa `mac_sha256_attack.py`? Quantos bytes tem? Pode consultar o esquema de padding para o `SHA256` no standard [RFC 6234](https://datatracker.ietf.org/doc/html/rfc6234#section-4.1).

## Cifras Autenticadas

Pretende-se melhorar a funcionalidade no programa de cifra de ficheiros da semana anterior para garantir simultaneamente a *confidencialidade* e a *integridade* dos dados.

Numa primeira abordagem, vamos estabelecer essas garantias combinando as técnicas criptográficas já estudadas: _cifra simétrica_ e _MAC_. A 
questão que surge é como combinar essas primitivas, sendo que é concebível considerar diferentes possibilidades:

 * **encrypt-and-MAC**: onde tanto cifra como o MAC são aplicados sobre o texto limpo;
 * **encrypt-then-MAC**: onde o texto limpo passa originalmente pela cifra, e o MAC é calculado já sobre o criptograma;
 * **MAC-then-encrypt**: onde é primeiro calculado o MAC sobre o texto limpo, e só depois é cifrado (texto limpo e _tag_ de autenticação).

Na realidade, a garantias de segurança obtidas diferem consideravelmente -- a alternativa **encrypt-then-MAC** é a que oferece melhores garantias, sendo que a alternativa **encrypt-and-MAC** é normalmente considerada "insegura" e a alternativa **MAC-then-encrypt** é normalmente considerada frágil em termos de implementação.

### PROG: `pbenc_aes_ctr_hmac.py`

Adapte o programa `pbenc_chacha20.py` realizado no guião anterior por forma utilizar a cifra AES no modo CTR e adicionar um MAC segundo a estratégia **encrypt-then-MAC**. Sugere-se a utilização do [HMAC](https://cryptography.io/en/latest/hazmat/primitives/mac/hmac/), definido sobre a função de hash `SHA256`.

> [!NOTE]
> Irá precisar de uma nova chave simétrica para o MAC (em criptografia, nunca se devem reutilizar chaves criptográficas para fins distintos). Isso pode ser facilmente ultrapassado solicitando "mais bytes" à KDF utilizada para derivar a chave.

### PROG: `pbenc_aes_gcm.py`

Actualmente, a generalidade das bibliotecas criptográficas já oferecem a funcionalidade de **[Cifra Autenticada](https://cryptography.io/en/latest/hazmat/primitives/aead/#)**, que combina as garantias de confidencialidade e integridade, em modos de funcionamento próprios e/ou em combinações pré-definidas.

Adapte a solução da alínea anterior para fazer uso da cifra autenticada [AES-GCM](https://cryptography.io/en/latest/hazmat/primitives/aead/#cryptography.hazmat.primitives.ciphers.aead.AESGCM).

### QUESTÃO: Q2

Internamente, a cifra AES-GCM usa também a cifra AES no modo CTR. No entanto, os seus comportamentos são significativamente diferentes. Qual a diferença -- ao nível do criptograma produzido -- entre cifrar a mesma mensagem com `pbenc_aes_ctr_hmac.py` ou com `pbenc_aes_gcm.py`? Justifique tendo em particular consideração o tamanho do ficheiro resultante e o que motiva essa diferença.

> [!TIP]
> Relembre que o modo CTR transforma uma cifra de blocos numa cifra de sequência, não sendo necessário adicionar padding às mensagens.