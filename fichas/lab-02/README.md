
# Lab 02

Controlo de Acesso ao Sistema de Ficheiros em Linux.


## 01 - Utilizador, Grupo e Permissão

Respostas dadas no ficheiro [sec1.sh](sec1.sh).


## 02 - Gestão de Utilizadores e de Grupos

Respostas dadas no ficheiro [sec2.sh](sec2.sh).


## 03 - Utilizador Real vs. Efetivo e Elevação de Privilégio

Respostas dadas no ficheiro [sec3.sh](sec3.sh).


## 04 - Listas Estendidas de Controlo de Acesso

Respostas dadas no ficheiro [sec4.sh](sec4.sh).


## 05 - Capabilities do Linux

#### Exercício 3

O resultado obtido é `Errr on bind: Permission denied`, pois em Linux certas portas são priviligiadas (<1024), isto é, só podem ser abertas com privilégios elevados, por exemplo **root**. O utilizador a executar o programa não tem essas permissões.

Para executar o programa na porta 80, podemos executar:
```shell
sudo setcap cap_net_bind_service=+ep ./webserver
./webserver 80
```
- `+p`: capability fica disponível
- `+e`: capability fica efetiva, isto é, ativada

Após executar `./webserver 80` vemos que já é possível fazer `bind()` à porta 80.
