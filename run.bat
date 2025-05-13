@echo off
echo ===============================
echo Iniciando ambiente do APE (Windows)
echo ===============================

REM 1) Cria o venv se não existir
if not exist ".venv" (
    echo Criando ambiente virtual...
    python -m venv .venv
)

REM 2) Ativa o venv
call .venv\Scripts\activate.bat

REM 3) Instala/upgrades das dependências
echo Instalando dependências...
pip install --upgrade pip
pip install -r requirements.txt

REM 4) Inicia o servidor Uvicorn
echo Iniciando servidor FastAPI...
uvicorn main:app --host 0.0.0.0 --port 8000 --reload


