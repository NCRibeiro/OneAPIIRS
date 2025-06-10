#!/usr/bin/env bash
set -e

echo "==============================="
echo " Iniciando ambiente do APE (Linux/macOS)"
echo "==============================="

# 1) Cria o ambiente virtual, se não existir
if [ ! -d ".venv" ]; then
  echo "Criando ambiente virtual..."
  python3 -m venv .venv
fi

# 2) Ativa o venv
source .venv/bin/activate

# 3) Instala dependências
echo "Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt

# 4) Verifica estrutura
if [ -f scripts/check_estrutura.sh ]; then
  echo "Verificando estrutura do projeto..."
  bash scripts/check_estrutura.sh
fi

# 5) Inicia servidor
echo "Iniciando servidor FastAPI..."
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
