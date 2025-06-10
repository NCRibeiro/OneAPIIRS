# Makefile para APE Project

PROJECT_NAME=ape_project
COMPOSE_FILE=docker-compose.yml

# ─── Docker: Subir e controlar containers ─────────────────────

up: check-estrutura
	docker-compose -f $(COMPOSE_FILE) up --build

down:
	docker-compose -f $(COMPOSE_FILE) down -v

rebuild:
	docker-compose -f $(COMPOSE_FILE) down -v
	docker-compose -f $(COMPOSE_FILE) build --no-cache
	docker-compose -f $(COMPOSE_FILE) up

ps:
	docker ps

sh:
	docker exec -it ape-api sh

# ─── Testes e Qualidade ───────────────────────────────────────

test:
	docker-compose run --rm tests

lint:
	flake8 . && isort --check-only . && black --check .

format:
	isort . && black .

typecheck:
	mypy .

# Roda verificação completa da qualidade (formatação, lint, tipagem, testes)
check-quality:
	./scripts/check_quality.sh

coverage:
	pytest --cov=app --cov-report=term --cov-report=html

# ─── Estrutura ────────────────────────────────────────────────

check-estrutura:
	./scripts/check_estrutura.sh

# ─── Ambiente local (opcional) ────────────────────────────────

install-prod:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt

# ─── Utilitários ──────────────────────────────────────────────

clean:
	docker system prune -af


## Flutter targets
.PHONY: flutter flutter-run flutter-build flutter-clean

flutter:
	@cd flutter && flutter pub get

flutter-run:
	@cd flutter && flutter run

flutter-build:
	@cd flutter && flutter build web

flutter-clean:
	@cd flutter && flutter clean

