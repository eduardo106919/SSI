# Semana 06

Cifras Modernas.

## Programa `cfich_chacha20.py`

#### Questão 01

A utilização de um _nonce_ fixo em cifras sequenciais compromete a segurança do sistema, pois resulta na reutilização do mesmo _keystream_ para diferentes mensagens sob a mesma chave. Tecnicamente, a cifra de fluxo gera uma sequência pseudoaleatória que é combinada com o texto-limpo através da operação XOR ($P \oplus K = C$). Se o par (chave, _nonce_) for repetido, um atacante que intersete dois criptogramas ($C_1$ e $C_2$) pode realizar a operação $C_1 \oplus C_2$, o que anula o _keystream_ e resulta no XOR dos dois textos-limpos originais ($P_1 \oplus P_2$). Esta vulnerabilidade, permite a recuperação parcial ou total das mensagens através de análise de frequência ou conhecimento de fragmentos de um dos textos, eliminando a propriedade de confidencialidade.

#### Questão 02

A cifra ChaCha20 opera como uma cifra sequencial síncrona, onde o _keystream_ é gerado independentemente do conteúdo da mensagem. Devido à natureza bit a bit da operação XOR utilizada na cifragem, a alteração de exatamente um bit no texto-limpo de entrada resultará na alteração de apenas um bit correspondente no criptograma de saída, na mesma posição relativa. Este fenómeno demonstra a ausência total de difusão, uma vez que não existe propagação de erro ou influência mútua entre os bits do bloco.

Exemplo:

```bash
$ echo "seguranca de sistemas informaticos" >> ssi.txt
$ python cfich_chacha20.py setup chave.key
Chave gerada e guardada em: chave.key
$ python cfich_chacha20.py enc ssi.txt chave.key
Ficheiro cifrado: ssi.txt.enc
$ hexer ssi.txt.enc              # alterar byte ...
$ python cfich_chacha20.py dec ssi.txt.enc chave.key
Ficheiro decifrado: ssi.txt.enc.dec
$ cat ssi.txt.enc.dec
seMuranca de sistemas informaticos
```

Podemos verificar que uma letra foi modificada na mensagem, mas as restantes não alteraram.

## Programa `chacha20_int_attack.py`

Exemplo de utilização:

```bash
$ echo "Pagar: 0100 EUR ao cliente A" >> transf.txt
$ python cfich_chacha20.py setup chave.key
Chave gerada e guardada em: chave.key
$ python cfich_chacha20.py enc transf.txt chave.key
Ficheiro cifrado: transf.txt.enc
$ python chacha20_int_attck.py transf.txt.enc 7 "0100" "9999"
Ataque concluído. Ficheiro gravado em: transf.txt.enc.attck
$ python cfich_chacha20.py dec transf.txt.enc.attck chave.key
Ficheiro decifrado: transf.txt.enc.attck.dec
$ cat transf.txt.enc.attck.dec
Pagar: 9999 EUR ao cliente A
```

## Programa `cfich_aes_cbc.py` e `cfich_aes_ctr.py`

### Questão 03

No modo **CTR**, a alteração de um bit no criptograma afeta apenas **um bit** na mensagem decifrada, na mesma posição, devido à sua natureza de cifra de fluxo. No modo **CBC**, o impacto é duplo: a alteração de um bit num bloco do criptograma corrompe completamente o bloco de texto-limpo correspondente (devido à difusão interna da cifra de bloco) e altera exatamente **um bit** no bloco de texto-limpo seguinte (devido à operação XOR entre o criptograma anterior e a saída da decifração).

### Questão 04

O impacto do programa `chacha20_int_attck.py` será de sucesso total no **AES-CTR**, uma vez que este modo é matematicamente equivalente à ChaCha20 no que toca à maleabilidade baseada em XOR. No **AES-CBC**, o ataque falhará no objetivo de "alterar uma informação específica": ao modificar o criptograma para tentar alterar um texto-limpo, o atacante acabará por destruir no bloco onde a alteração é feita. Embora o bit pretendido possa ser alterado no bloco seguinte, a corrupção do bloco atual torna o ataque detetável ou inútil.

## Programa `pbenc_chacha20.py`

#### Questão 05

O **salt** e o **nonce** desempenham funções distintas e cruciais, sendo ambos estritamente necessários em conjunto. O **salt** é utilizado pela _Key Derivation Function_ para garantir que _pass-phrases_ idênticas resultem em chaves criptográficas diferentes. O **nonce** é utilizado para garantir que a mesma chave, quando aplicada a diferentes mensagens, ou à mesma mensagem em momentos distintos, produza _keystreams_ únicos, impedindo ataques de reutilização de _keystream_. Mesmo que o utilizador use a mesma password para vários ficheiros, o **salt** garante que a chave mestre seja diferente para cada um; simultaneamente, o **nonce** assegura a unicidade estatística da operação de XOR, protegendo a integridade da cifra de fluxo.
