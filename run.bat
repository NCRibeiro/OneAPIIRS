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

REM 3) Instala/atualiza dependências
echo Instalando dependências...
pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt

REM 4) Valida estrutura (opcional)
if exist scripts\check_estrutura.sh (
    echo Verificando estrutura do projeto...
    bash scripts/check_estrutura.sh
)

REM 5) Inicia o servidor Uvicorn
echo Iniciando servidor FastAPI...
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
