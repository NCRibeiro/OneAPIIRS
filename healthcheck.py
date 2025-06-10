import os
import re
import sys
import configparser
from typing import Optional

import typer
from rich import print
from fastapi import APIRouter
from core.settings import settings
from app.routes import api_router

app = typer.Typer(help="HealthCheck CLI para o projeto OneAPIIRS")
router = APIRouter()


@router.get("/ping")
async def ping() -> dict[str, str]:

    return {"status": "alive", "message": "pong"}


@app.command()
def fix_env(env_path: str = ".env") -> None:
    print(f"[bold cyan] Verificando {env_path}...[/bold cyan]")
    if not os.path.exists(env_path):
        print("[red] Arquivo .env não encontrado. Criando exemplo básico.[/red]")
        with open(env_path, "w") as f:

            f.write("ONEAPIIRS_SECRET_KEY=changeme\n")
        return

    with open(env_path, "r") as f:
        lines = f.readlines()

    fixed_lines = []
    for line in lines:
        line = re.sub(r"\s+#.*", "", line)
        if "=" not in line:
            continue
        key, value = line.strip().split("=", 1)
        if value.lower() in ["true", "false"]:
            value = value.lower()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        fixed_lines.append(f"{key}={value}\n")

    with open(env_path, "w") as f:

        f.writelines(fixed_lines)

    print("[green] .env validado e corrigido.[/green]")


@app.command()
def check_settings(file: str = "core/settings.py") -> None:
    print(f"[bold cyan] Verificando {file}...[/bold cyan]")
    if not os.path.exists(file):
        print("[red] settings.py não encontrado.[/red]")
        return

    with open(file, "r") as f:
        content = f.read()

    if "@validator" in content:
        print("[yellow] Encontrado '@validator'. Use '@field_validator' no Pydantic v2.[/yellow]")

    if "BaseSettings" in content and "pydantic_settings" not in content:
        print("[yellow] BaseSettings não importado corretamente de pydantic_settings.[/yellow]")

    print("[green] settings.py checado.[/green]")


@app.command()
def check_docker(file: str = "docker-compose.yml") -> None:
    print(f"[bold cyan] Verificando {file}...[/bold cyan]")
    if not os.path.exists(file):
        print("[red] docker-compose.yml não encontrado.[/red]")
        return

    with open(file, "r") as f:
        content = f.read()

    if "env_file:" not in content:
        print("[yellow] docker-compose.yml não referencia um .env[/yellow]")
    else:
        print("[green] docker-compose.yml usa env_file.[/green]")

    if "postgres" not in content:
        print("[yellow] Serviço de banco de dados não encontrado.[/yellow]")

    print("[green] docker-compose.yml validado.[/green]")


@app.command()
def check_ini(file: str = "config_env.ini") -> None:
    print(f"[bold cyan] Verificando {file}...[/bold cyan]")
    if not os.path.exists(file):
        print("[yellow]ℹ config_env.ini não encontrado (opcional).[/yellow]")
        return

    config = configparser.ConfigParser()
    config.read(file)

    if "DEFAULT" not in config:
        print("[red] config_env.ini precisa começar com [DEFAULT][/red]")
        return

    keys = [
        "SECRET_KEY", "REFRESH_SECRET_KEY", "DATABASE_URL",
        "APP_ENV", "DEBUG", "RELOAD"
    ]
    for key in keys:
        if key not in config["DEFAULT"]:
            print(f"[yellow] Faltando {key} em config_env.ini[/yellow]")

    print("[green] config_env.ini validado.[/green]")


@app.command()
def check_imports() -> None:
    print("[bold cyan] Testando imports...[/bold cyan]")
    try:
        _ = settings

        print("[green] Importação de settings OK[/green]")
    except Exception as e:
        print(f"[red] Erro na importação de settings: {e}[/red]")

    try:
        _ = api_router

        print("[green] Importação de api_router OK[/green]")
    except Exception as e:
        print(f"[red] Erro na importação de api_router: {e}[/red]")


@app.command()
def full() -> None:
    fix_env()
    check_ini()
    check_settings()
    check_docker()
    check_imports()
    print("[bold green] Verificação completa finalizada![/bold green]")


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check-imports"
    if cmd == "check-imports":
        check_imports()
    elif cmd == "full":
        full()
    else:
        print(f"Comando desconhecido: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
