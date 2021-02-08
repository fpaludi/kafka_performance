GREEN=\033[0;32m
NC=\033[0m

BASE_COMPOSE_FILE=docker/docker-compose.yml

export NETWORK_NAME=kafka_perfo
NETWORKS=$(shell docker network ls --filter name=^${NETWORK_NAME} --format="{{ .Name }}")

BASE_COMPOSE_CMD=docker-compose -f $(CURDIR)/$(BASE_COMPOSE_FILE)

create_network:
	@if [ -z $(NETWORKS) ]; then \
		echo '${GREEN}Creating network '$(NETWORK_NAME)'${NC}'; \
		docker network create $(NETWORK_NAME); \
	else \
		echo '${GREEN} Network '$(NETWORK_NAME)' already exists${NC}'; \
	fi;

build: create_network
	$(BASE_COMPOSE_CMD) build

stop:
	$(BASE_COMPOSE_CMD) down --remove-orphans

run:
	$(BASE_COMPOSE_CMD) up -d
