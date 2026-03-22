# Semana 6: Cifras Modernas

Este guião pressupõe a utilização da biblioteca python `cryptography` (https://cryptography.io/en/stable/).

O objetivo deste guião é cifrar o conteúdo de um ficheiro, assegurando a *confidencialidade* dos dados lá armazenados. Para tal iremos experimentar diferentes cifras, por forma a melhor percebermos as suas propriedades.

### PROG: `cfich_chacha20.py`

Defina o programa `cfich_chacha20.py` que cifra um ficheiro usando a cifra sequencial [`ChaCha20`](https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#cryptography.hazmat.primitives.ciphers.algorithms.ChaCha20). O programa receba como argumentos:
 * o tipo de operação a realizar: `setup`, `enc` ou `dec`
   - `setup <fkey>` cria ficheiro contendo uma chave apropriada para a cifra `Chacha20` (com nome `<fkey>`)
   - `enc <fich> <fkey>` cifra ficheiro passado como argumento `<fich>`, usando a chave lida do ficheiro `<fkey>`. O criptograma resultante deverá ser gravado `<fich>.enc` (i.e. adiciona a extensão `.enc` ao nome do ficheiro de texto-limpo).
   - `dec <fich> <fkey>` decifra criptograma contido em `<fich>`, usando a chave lida do ficheiro `<fkey>`. Armazena o texto-limpo recuperado num ficheiro com nome `<fich>.dec`.
   
> [!TIP]
> Relembre que cifras sequenciais devem ser sempre utilizadas com um *NONCE* e note que isso está refletido na API da cifra. Será necessário utilizar o mesmo *NONCE* para cifrar e decifrar, pelo que o deve gravar juntamente com o criptograma.

### QUESTÃO: Q1

Qual o impacto de se considerar um *NONCE* fixo (e.g. tudo `0`)? Que implicações terá essa prática na segurança da cifra?


### QUESTÃO: Q2

A cifra `ChaCha20`, por se tratar de uma **cifra sequencial síncrona**, não promove difusão (influência de bits de input no criptograma).
Crie uma mensagens e cifre-a. Altere apenas um bit da mensagem original e cifre-a com a mesma chave (e *NONCE*).
Alterar um bit do texto-limpo de input afeta quantos bits do criptograma de output?

> [!TIP]
> Pode utilizar um editor como o `hexer` (que funciona como o `vim` mas para hexadecimal) para modificar um bit num ficheiro.
> Pode utilizar o comando  `vbindiff file1 file2` para visualizar facilmente a diferença entre dois ficheiros binários `file1` e `file2`.

### PROG: `chacha20_int_attck.py`

A cifra `ChaCha20`, por si só, não garante integridade dos dados.
O propósito do programa `chacha20_int_attck.py` é ilustrar como pode ser manipulada a informação cifrada pelo programa anterior -- se soubermos um fragmento do conteúdo de uma dada posição do texto-limpo, podemos alterar essa informação. O programa `chacha20_int_attck.py`deve então receber os seguintes argumentos: `<fctxt> <pos> <ptxtAtPos> <newPtxtAtPos>`, sendo que `<fctxt>` é o nome do ficheiro contendo o criptograma; `<pos>` é a posição onde sabemos ter sido cifrado `<ptxtAtPos>`, e `<newPtxtAtPos>` é o que se pretende vir a obter quando se decifrar o ficheiro. O criptograma manipulado deve ser gravado no ficheiro com nome `<fctxt>.attck`.


### PROG: `cfich_aes_cbc.py` e `cfich_aes_ctr.py`

Defina novas versões do programa que cifra ficheiros para utilizar a cifra por blocos [`AES`](https://cryptography.io/en/stable/hazmat/primitives/symmetric-encryption/#cryptography.hazmat.primitives.ciphers.algorithms.AES), nos modos [`CBC`](https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#cryptography.hazmat.primitives.ciphers.modes.CBC) e [`CTR`](https://cryptography.io/en/stable/hazmat/primitives/symmetric-encryption/#cryptography.hazmat.primitives.ciphers.modes.CTR).

> [!NOTE]
> O modo CBC necessita que o texto limpo tenha um tamanho múltiplo do tamanho do bloco (16 bytes, no caso do AES). Deve por isso usar [Padding](https://cryptography.io/en/stable/hazmat/primitives/padding/#module-cryptography.hazmat.primitives.padding).

### QUESTÃO: Q3

Um ataque a uma cifra (não autenticada) consiste tipicamente em executar *bit flips*: tentar executar modificações no criptograma sem ter que conhecer a chave.
Para cada um dos modos CBC e CTR, se alterar um bit de um criptograma, quantos bits afeta na mensagem original após decifrar?

> [!NOTE]
> No modo CBC os primeiros 16 bytes do criptograma correspondem ao IV.

### QUESTÃO: Q4

Qual o impacto de utilizar o programa `chacha20_int_attck.py` nos criptogramas produzidos pelos programas `cfich_aes_cbc.py` e `cfich_aes_ctr.py`? Comente e justifique a sua resposta.

### PROG: `pbenc_chacha20.py`

Armazenar segredos cryptográficos em ficheiros sem estarem devidamente protegidas **é uma má prática**. Em vez disso, deve-se:

 1. Derivar os segredos a partir de uma *pass-phrase* com recurso a uma [Key Derivation Functions (KDF)](https://cryptography.io/en/stable/hazmat/primitives/key-derivation-functions/#module-cryptography.hazmat.primitives.kdf) -- o que se designa por **Password-Based Encryption**, ;
 2. Armazenar em ficheiros devidamente protegidos (aka *keystore*), esta por sua vez recorrendo a *Password-Based Encryption* para a sua própria protecção.

Pretende-se assim alterar o programa `cfich_chacha20.py` para suportar *Password-Based Encryption*. Deixa portanto de existir o comando para gerar uma nova chave, e as opções `enc` e `dec` deixam de receber o nome do ficheiro da chave como argumento. Em vez disso, leem de `stdin` a *pass-phrase* que permitirá derivar a chave usada na cifra. Sugere-se a utilização da KDF [`PBKDF2`](https://cryptography.io/en/stable/hazmat/primitives/key-derivation-functions/#cryptography.hazmat.primitives.kdf.pbkdf2.PBKDF2HMAC).

> [!TIP]
> Relembre que password-based encryption deve usar sempre um valor de *salt*, que deve também ser armazenado juntamente com o criptograma.

### QUESTÃO: Q5

Qual a função do *salt* e do *NONCE* na versão de password-based encryption do `ChaCha20`? São ambos necessários conjuntamente?