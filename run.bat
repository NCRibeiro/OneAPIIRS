@echo off
echo ===============================
echo Iniciando ambiente do APE (Windows)
echo ===============================

REM Cria ambiente virtual se ainda não existir
if not exist ".venv" (
    echo Criando ambiente virtual...
    python -m venv .venv
)

REM Ativa o ambiente virtual
call .venv\Scripts\activate.bat

REM Instala as dependências
echo Instalando dependências...
pip install --upgrade pip
pip install -r requirements.txt

REM Inicia a API com Uvicorn
echo Iniciando servidor FastAPI...
uvicorn app.main:app --reload

