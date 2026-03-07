#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>

#define BUF_SIZE 4096

static void write_str(int fd, const char *s) {
    write(fd, s, strlen(s));
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        write_str(STDERR_FILENO, "Uso: cat1 <ficheiro>\n");
        return 1;
    }

    int fd = open(argv[1], O_RDONLY);
    if (fd < 0) {
        write_str(STDERR_FILENO, "Erro ao abrir ficheiro: ");
        write_str(STDERR_FILENO, strerror(errno));
        write_str(STDERR_FILENO, "\n");
        return 2;
    }

    char buf[BUF_SIZE];
    ssize_t n;

    while ((n = read(fd, buf, sizeof(buf))) > 0) {
        ssize_t off = 0;
        while (off < n) {
            ssize_t w = write(STDOUT_FILENO, buf + off, (size_t)(n - off));
            if (w < 0) {
                write_str(STDERR_FILENO, "Erro a escrever: ");
                write_str(STDERR_FILENO, strerror(errno));
                write_str(STDERR_FILENO, "\n");
                close(fd);
                return 3;
            }
            off += w;
        }
    }

    if (n < 0) {
        write_str(STDERR_FILENO, "Erro a ler ficheiro: ");
        write_str(STDERR_FILENO, strerror(errno));
        write_str(STDERR_FILENO, "\n");
        close(fd);
        return 4;
    }

    close(fd);
    return 0;
}

