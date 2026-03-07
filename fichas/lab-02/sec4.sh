#!/bin/bash

# Exercício 1
getfacl porto.txt

# Exercício 2
setfacl -m g:grupo-ssi:w porto.txt

# Exercício 3
getfacl porto.txt
# Antes de executar o comando setfacl vemos que o ficheiro porto.txt tem apenas as permissões "tradicionais" (dono, grupo e outros). Após executar o comando setfacl vemos que o ficheiro tem mais duas entradas, uma correspondente às permissões para grupo-ssi. A outra entrada (mask::rw-) corresponde à máscara de permissões efetivas, isto é, corresponde a um limite superior de permissões efetivas.

# Exercício 4
su user1
cat "rio douro" >> porto.txt
cat porto.txt
# O utilizador user1 (ou qualquer utilizador do grupo-ssi) não consegue visualizar o conteúdo do ficheiro, pois o grupo-ssi tem apenas permissões de escrita. Tal é visivel no resultado do exercicio anterior. Este comportamento já era de esperar dado que apenas demos permissões de escrita ao grupo-ssi.

