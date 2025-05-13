#!/usr/bin/env bash
set -e

echo "1) Formatação (Black)…"
black --check .

echo "2) Importação (isort)…"
isort --check-only .

echo "3) Lint (flake8)…"
flake8 .

echo "4) Tipos (mypy)…"
mypy app

echo "5) Padrões (pylint)…"
pylint app

echo "6) Testes (pytest)…"
pytest --maxfail=1 --disable-warnings -q

echo "Tudo conferido!"
