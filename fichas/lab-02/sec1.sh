#!/bin/bash

# Exercício 1
touch lisboa.txt porto.txt braga.txt
echo "hello from lisboa" >> lisboa.txt
echo "hello from porto" >> porto.txt
echo "hello from braga" >> braga.txt

# Exercício 2
ls -l lisboa.txt

# Exercício 3
chmod a+rw lisboa.txt

# Exercício 4
chmod u=rx porto.txt 

# Exercício 5
chmod u+r,go-r braga.txt

# Exercício 6
mkdir -p dir1 dir2
ls -ld dir1 dir2

# Exercício 7
chmod go-x dir2

