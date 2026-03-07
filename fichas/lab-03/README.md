
# Lab 03

Demonstração de Exploits Relativos a Controlo de Acesso.


## 01 - Capability Leaking

#### Exercício 2

Após executar o programa `backupssi` a diretoria `/root` é aberta para leitura e criada uma pasta chamada `backupssi` e por fim é iniciada uma shell, deixando o processo a correr. O descritor da pasta `/root` não é terminado. O utilizador pode executar um programa na shell que tira proveito desse descritor aberto.

#### Exercício 3

Resposta dada no ficheiro [`exploit_backupssi.c`](exploit_backupssi.c).

#### Exercício 4

Correção efetuada no ficheiro [`backupssi.c`](backupssi.c).

A correção efetuada consiste em fechar o descritor para a diretoria `/root`, pois evita que o processo continue a ter acesso à diretoria através do descritor.


## 02 - Elevação de Privilégio

#### Exercício 2

A vulnerabilidade consiste no facto de o descritor para o ficheiro `/etc/passwd` não ser fechado, principalmente pelo facto de ter sido aberto para escrita.

#### Exercício 3

Exploit presente no ficheiro [`exploit_passwdleak.c`](exploit_passwdleak.c).

O ficheiro `/etc/passwd` contém a listagem dos utilizadores do sistema. Ao adicionar uma entrada neste ficheiro estamos a adicionar um utilizador ao sistema, operação que deve ser feita com consciência.

#### Exercício 4

Ao conseguir adicionar `ssihacker::0:0::/root:/bin/sh` ao `/etc/passwd`, passa a existir um utilizador equivalente a **root** (`UID=0` e `GID=0`), isto é, tem os privilégios de root, logo é capaz de ler e escrever qualquer ficheiro, alterar permissões de outros utilizadores, etc.

#### Exercício 5

Correção efetuada no ficheiro [`passwdleak.c`](passwdleak.c).

Ao fechar o descritor de ficheiro antes de abrir a shell, a shell não herda o descritor, logo não será possível efetuar escritas no ficheiro.
