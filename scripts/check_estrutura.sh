#!/bin/bash

echo "Verificando estrutura do projeto APE…"

check_file() {
  if [ -f "$1" ]; then
    echo "OK: Arquivo '$1' encontrado."
  else
    echo "ERRO: Arquivo '$1' não encontrado."
    exit 1
  fi
}

check_dir() {
  if [ -d "$1" ]; then
    echo "OK: Pasta '$1' encontrada."
  else
    echo "ERRO: Pasta '$1' não encontrada."
    exit 1
  fi
}

# 1) main.py na raiz
check_file "main.py"

# 2) requirements.txt na raiz
check_file "requirements.txt"

# 3) Pastas principais
check_dir "app/core"
check_dir "app/routes"
check_dir "app/db"
check_dir "app/scripts"

echo "Estrutura verificada com sucesso. Nenhum problema encontrado."
