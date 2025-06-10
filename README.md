# OneAPIIRS - O Futuro da Transformação Fiscal Digital

![Build Status](https://github.com/seu-usuario/OneAPIIRS/actions/workflows/ci-tests.yml/badge.svg)
![Cobertura de Testes](https://img.shields.io/badge/Cobertura-90%25-brightgreen)

**OneAPIIRS** não é apenas uma API — é a revolução digital na transformação de dados fiscais. Imagine um sistema inteligente que integra dados fiscais de sistemas legados complexos e os transforma em informações modernas e acessíveis, tudo em tempo real. Projetada para empresas, governos e instituições fiscais que estão prontas para abraçar o futuro da tributação com precisão e segurança.

## A Missão

Modernizar sistemas fiscais através da transformação de dados legados em informações seguras, acessíveis e auditáveis. O OneAPIIRS integra inteligência fiscal para detectar inconsistências, prevenir fraudes e permitir análises modernas e relatórios dinâmicos.

## Características Principais

- ✨ **Transformação de Dados Legados** com suporte a formatos COBOL e outros.
- 🤖 **Auditoria Fiscal Inteligente** com detecção automática de fraudes e inconsistências.
- 🔬 **Relatórios Preditivos** com dashboards interativos usando Plotly Dash.
- 🔐 **Segurança Avançada** com JWT, CSRF, e testes automatizados.
- ⚖️ **Arquitetura Containerizada** com Docker, PostgreSQL e FastAPI.

## Tecnologias Utilizadas

- FastAPI
- PostgreSQL
- Docker / Docker Compose
- JWT Authentication
- Plotly Dash
- Python 3.10+
- Black, Flake8, Isort, Mypy, Pytest

## Como Rodar Localmente

### Requisitos
- Python 3.10+
- Docker e Docker Compose
- Git

### Execução com Makefile

```bash
make up          # Sobe o sistema com validação de estrutura
make test        # Executa testes automatizados
make check-quality  # Verifica formatação, tipo, lint e testes
make sh          # Entra no container da API
```

## Scripts Disponíveis

- `scripts/check_estrutura.sh` — Valida se a estrutura do projeto está correta.
- `scripts/check_quality.sh` — Executa: black, isort, flake8, mypy, pylint, pytest.

## Testes Automatizados

Os testes cobrem repositórios em memória, autenticação JWT, auditorias fiscais e consistência de dados. Executados com `pytest`:

```bash
make test
```

Gera cobertura HTML:
```bash
make coverage
```
Abra em:
```bash
xdg-open htmlcov/index.html  # Linux
open htmlcov/index.html      # macOS
start htmlcov/index.html     # Windows
```

## Documentação da API

Acesse:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## Contribuição

Este projeto é desenvolvido de forma independente. Não há equipe, apenas o código, a visão e a missão de transformar a gestão fiscal digital.

---

✅ Repositório mantido por [@NCRibeiro](https://github.com/NCRibeiro)

> **Atenção:** Este projeto é protegido por copyright. Uso comercial ou redistribuição proibidos sem autorização.
© 2025 Nívea Ribeiro. Todos os direitos reservados.

