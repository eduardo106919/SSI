# Lab 04

Cifras Clássicas.

## Cifra de César

Cifra de César implementada no ficheiro [cesar.py](cesar.py).

Ataque à cifra de César implementada no ficheiro [attack_cesar.py](attack_cesar.py).

## Cifra de Vigenère

Cifra de Vigenère implementada no ficheiro [vigenere.py](vigenere.py).

Ataque à cifra de Vigenère implementada no ficheiro [attack_vigenere.py](attack_vigenere.py).

## One Time Pad

#### Questão 02

Não. A segurança absoluta da One-Time Pad baseia-se na premissa de que a chave é perfeitamente aleatória e nunca reutilizada. Ao utilizar o bad_prng, violamos o requisito de aleatoriedade, pois a chave torna-se previsível a partir de uma semente pequena. O ataque ataca a implementação deficiente do gerador, não o princípio matemático da cifra.

#### Questão 03

Se usarmos a mesma chave $K$ para cifrar $M_1$ e $M_2$, obtemos $C_1 = M_1 \oplus K$ e $C_2 = M_2 \oplus K$.
Ao fazer o XOR dos dois criptogramas:

$$C_1 \oplus C_2 = (M_1 \oplus K) \oplus (M_2 \oplus K) = M_1 \oplus M_2$$

Isso elimina a chave e revela a relação binária entre as duas mensagens originais. É possível construir um ataque (conhecido como _Many-Time Pad attack_), pois técnicas de análise de frequência e padrões linguísticos podem ser usadas no resultado de $M_1 \oplus M_2$ para recuperar ambos os textos originais.
