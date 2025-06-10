#!/usr/bin/env bash
set -e

echo "🔍 Verificação de Qualidade do Projeto APE"

echo "🎨 1) Formatação (Black)…"
black --check .

echo "📚 2) Ordenação de Imports (isort)…"
isort --check-only .

echo "🧼 3) Lint (flake8)…"
flake8 .

echo "🧠 4) Tipagem (mypy)…"
mypy app

if command -v pylint &> /dev/null; then
  echo "🔎 5) Regras Avançadas (pylint)…"
  pylint app
else
  echo "⚠️  Pylint não encontrado. Ignorando etapa 5."
fi

echo "🧪 6) Testes Automatizados (pytest)…"
pytest --maxfail=1 --disable-warnings -q

echo "✅ Tudo conferido com sucesso!"
