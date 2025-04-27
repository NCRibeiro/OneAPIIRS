#!/bin/bash

echo "Verificando estrutura do projeto APE..."

# Verifica se main.py está dentro da pasta app/
if [ ! -f "app/main.py" ]; then
  echo "ERRO: O arquivo 'main.py' não está dentro da pasta 'app/'"
  echo "Solução: Mova o arquivo 'main.py' para a pasta correta: app/main.py"
  exit 1
else
  echo "OK: 'app/main.py' encontrado."
fi

# Verifica se requirements.txt existe
if [ ! -f "requirements.txt" ]; then
  echo "ERRO: O arquivo 'requirements.txt' está faltando na raiz do projeto."
  exit 1
else
  echo "OK: 'requirements.txt' encontrado."
fi

# Verifica se pasta core existe
if [ ! -d "app/core" ]; then
  echo "ERRO: Pasta 'app/core' não encontrada."
  exit 1
else
  echo "OK: Pasta 'app/core' encontrada."
fi

# Verifica se pasta api existe
if [ ! -d "app/api" ]; then
  echo "ERRO: Pasta 'app/api' não encontrada."
  exit 1
else
  echo "OK: Pasta 'app/api' encontrada."
fi

echo "Estrutura verificada com sucesso. Nenhum problema encontrado."
