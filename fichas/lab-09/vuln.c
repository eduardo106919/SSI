#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void secret_function(void)
{
    printf("\n[!] ACCESS GRANTED: you reached the secret function!\n");
    printf("[!] In a real exploit, this could be arbitrary code execution.\n\n");
    exit(0);
}

void process_input(char *input)
{
    char buffer[64];
    size_t len = strlen(input);

    /* Verificação explícita de comprimento */
    if (len >= sizeof(buffer))
    {
        fprintf(stderr, "[!] Erro: input demasiado longo (%zu bytes, máximo %zu).\n",
                len, sizeof(buffer) - 1);
        exit(EXIT_FAILURE);
    }

    /* Substituir strcpy por alternativa segura */
    strncpy(buffer, input, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';

    printf("[*] You entered: %s\n", buffer);
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        fprintf(stderr, "Usage: %s <input>\n", argv[0]);
        return 1;
    }
    printf("[*] process_input return address is on the stack.\n");
    process_input(argv[1]);
    printf("[*] Normal programme termination.\n");
    return 0;
}
