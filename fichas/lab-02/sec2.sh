#!/bin/bash

# Exercício 0
cat /etc/passwd
cat /etc/group

# Exercício 1
sudo adduser user1
sudo adduser user2
sudo adduser user3

# Exercício 2
sudo groupadd grupo-ssi
sudo usermod -aG grupo-ssi user1
sudo usermod -aG grupo-ssi user2
sudo usermod -aG grupo-ssi user3

sudo groupadd par-ssi
sudo usermod -aG par-ssi user2
sudo usermod -aG par-ssi user3

# Exercício 3
# Após executar "cat /etc/passwd" vemos a presença de três novos utilizadores (user1, user2, user3).
# Após executar "cat /etc/group" vemos a presença de dois novos grupos (grupo-ssi e par-ssi) que contém os utilizadores (user1, user2, user3) e (user2, user3) respetivamente.

# Exercício 4
sudo chown user3 braga.txt

# Exercício 5
cat braga.txt
# O resultado é:
# cat: braga.txt: Permission denied
# pois apenas o dono do ficheiro (user3) tem permissões de leitura, e o utilizador atual não é o dono do ficheiro.

# Exercício 6
su user3

# Exercício 7
# Ao executar o comando "id" é apresentado o identificador do utilizador user3 e os identificadores dos grupos a que pertence (user3, grupo-ssi, par-ssi). A informação apresentada é do utilizador user3, pois foi iniciada uma sessão em seu nome.

# Exercício 8
cat braga.txt
# O conteúdo do ficheiro braga.txt já é visivel, pois o utilizador user3 é o dono do ficheiro e apenas ele tinha permissões de leitura. Na sessão anterior o utilizador não tinhas permissões de leitura, logo não poderia vizualizar o conteúdo do ficheiro.

# Exercício 9
cd dir2
# Não é possível mudar para a diretoria dir2, pois o utilizador user3 não tem permissões de execução. Como este não é o dono do ficheiro e não pertence ao grupo, user3 encaixa nas permissões dos outros utilizadores (others), e este conjunto de utilizadores apenas tem permissões de leitura, mas não tem permissão de execução.

