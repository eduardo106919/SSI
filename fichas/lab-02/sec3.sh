#!/bin/bash

# Exercício 1
gcc mycat.c -o mycat

# Exercício 2
sudo adduser userssi

# Exercício 3
sudo chown userssi mycat
sudo chown userssi braga.txt

# Exercício 4
./mycat braga.txt
# O ouput do programa executável apresenta um erro ao abrir o ficheiro, pois o utilizador atual não tem permissões de leitura.

# Exercício 5
sudo chmod u+s mycat

# Exercício 6
./mycat braga.txt
# Nesta execução já podemos ver o conteúdo do ficheiro braga.txt, pois estamos a executar o programa em nome do dono (userssi), isto é, apenas o dono do ficheiro pode-o executar, mas outros utilizadores têm permissão para executar o programa em nome do dono.

