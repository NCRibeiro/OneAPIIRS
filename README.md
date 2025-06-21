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


## Arquitetura Fullstack

  1. Backend: FastAPI + PostgreSQL + SQLAlchemy.

  2. Front‑end: Flutter para web e mobile.

  3. Orquestração de Contêineres: Docker Compose com serviços isolados.


## Infraestrutura na Google Cloud Platform (GCP)

Integração de Serviços

  . Cloud Run: deploy serverless da API.

  . Cloud Build & Container Registry: CI/CD e armazenamento de imagens Docker.

  . BigQuery: data warehouse para análises avançadas.

  . Pub/Sub: pipeline de eventos em tempo real (oneapiirs-events).

  . Cloud Storage: buckets para dados brutos e artefatos (oneapiirs-raw-data).


Passo a Passo para o Deploy

  1. Configurar CLI:

    gcloud auth login
    gcloud config set project $PROJECT_ID

  2. Build e Push da Imagem:

    gcloud builds submit --tag gcr.io/$PROJECT_ID/oneapiirs-api

  3. Deploy no Cloud Run:

    gcloud run deploy oneapiirs-api --image gcr.io/$PROJECT_ID/oneapiirs-api --plataform managed --region us-central1 --allow-unauthenticated --memory 512Mi

  4. Configuração de BigQuery:

    . Criar dataset oneapiirs e tabelas conforme o esquema de dados.
    . Conceder permissões ao serviço Cloud Run.

  5. Configuração de Pub/Sub:

    . Criar tópico oneapiirs-events.
    . Subscribes e políticas de acesso.

  6. Configuração de Cloud Storage:
    . Criar bucket oneapiirs-raw-data.
    . Definir permissões de leitura/gravação para o serviço.


## Tecnologias Utilizadas

  . Linguagens & Frameworks: Python 3.10+, FastAPI, Flutter.

  . Banco de Dados: PostgreSQL, BigQuery.

  . Contêineres: Docker, Docker Compose, Cloud Run.

  . Mensageria: Google Cloud Pub/Sub.

  . Armazenamento: Google Cloud Storage.

  . Visualização: Plotly Dash.

  . Qualidade de Código: Black, Isort, Flake8, Mypy, Pytest.


## Executando Localmente

Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- Git
- Flutter (SDK) instalado


## Backend

# No diretório raiz
Execução com Makefile

```bash
make up          # Sobe o sistema com validação de estrutura
make test        # Executa testes automatizados
make check-quality  # Verifica formatação, tipo, lint e testes
make sh          # Entra no container da API
```


## Front‑end Flutter

cd flutter
flutter pub get
flutter run -d chrome  # Web
# ou flutter run        # Mobile


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
- Swagger UI: http://localhost:8080/api/v1/docs
- ReDoc: http://localhost:8080/api/v1/redoc


## Contribuição

Este projeto é desenvolvido de forma independente. Não há equipe, apenas o código, a visão e a missão de transformar a gestão fiscal digital.

---

✅ Repositório mantido por [@NCRibeiro](https://github.com/NCRibeiro)

> **Atenção:** Este projeto é protegido por copyright. Uso comercial ou redistribuição proibidos sem autorização.
© 2025 Nívea Ribeiro. Todos os direitos reservados.

