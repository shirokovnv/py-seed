#!/usr/bin/make
# Makefile readme (en): <https://www.gnu.org/software/make/manual/html_node/index.html#SEC_Contents>

SHELL = /bin/sh
IMAGE_NAME = py-seed-in-docker
DOCKER_BIN = $(shell command -v docker 2> /dev/null)
COMPOSE_BIN = $(shell command -v docker-compose 2> /dev/null)

.PHONY : help build-image \
         pull shell install \
         up down
.SILENT : help
.DEFAULT_GOAL : help

# This will output the help for each task. thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install all app dependencies
	$(COMPOSE_BIN) run --no-deps web pip install --no-cache-dir --upgrade -r ./requirements.txt

shell: ## Start shell into web container
	$(COMPOSE_BIN) run web sh

build-image:
	$(DOCKER_BIN) build -f ./Dockerfile . -t $(IMAGE_NAME)

up:
	$(COMPOSE_BIN) up --detach --remove-orphans
	@printf "\n   \e[30;43m %s \033[0m\n\n" 'Server started: <http://127.0.0.1:8000>'

down:
	$(COMPOSE_BIN) down

pull: ## Pull latest images
	$(COMPOSE_BIN) pull