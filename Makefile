# Makefile para APE Project

PROJECT_NAME=ape_project
COMPOSE_FILE=docker-compose.yml

# Subir a aplicação
up:
	docker-compose -f $(COMPOSE_FILE) up --build

# Derrubar a aplicação
down:
	docker-compose -f $(COMPOSE_FILE) down -v

# Rebuild completo
rebuild:
	docker-compose -f $(COMPOSE_FILE) down -v
	docker-compose -f $(COMPOSE_FILE) build --no-cache
	docker-compose -f $(COMPOSE_FILE) up

# Executar apenas o Dashboard
dash:
	docker-compose -f $(COMPOSE_FILE) up --build --entrypoint "dash"

# Limpar imagens paradas
clean:
	docker system prune -af

# Verificar containers ativos
ps:
	docker ps

# Acessar container da API
sh:
	docker exec -it ape-api sh

# Verifica se a estrutura de pastas está correta
check-estrutura:
	./scripts/check_estrutura.sh
