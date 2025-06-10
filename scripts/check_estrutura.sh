#!/bin/bash

echo "🔍 Verificando estrutura do projeto APE…"

check_file() {
  if [ -f "$1" ]; then
    echo "✅ Arquivo '$1' encontrado."
  else
    echo "❌ ERRO: Arquivo '$1' não encontrado."
    exit 1
  fi
}

check_dir() {
  if [ -d "$1" ]; then
    echo "✅ Pasta '$1' encontrada."
  else
    echo "❌ ERRO: Pasta '$1' não encontrada."
    exit 1
  fi
}

# Raiz esperada do projeto
BASE_PATH=$(dirname "$0")/..

cd "$BASE_PATH" || exit 1

# Arquivos obrigatórios
check_file "main.py"
check_file "requirements.txt"
check_file "docker-compose.yml"
check_file "Dockerfile"
check_file ".flake8"
check_file "pytest.ini"
check_file "mypy.ini"

# Pastas principais
check_dir "app/core"
check_dir "app/routes"
check_dir "app/db"
check_dir "scripts"
check_dir "tests"

echo "✅ Estrutura verificada com sucesso. Nenhum problema encontrado."
