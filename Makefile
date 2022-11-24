THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help build up start down destroy stop restart logs logs-api ps login-timesc

build:
	docker-compose build $(c)

up:
	docker-compose up -d $(c)

up-dev:
	docker-compose -f docker-compose.dev.yml up -d $(c)

down:
	docker-compose down

run:
	docker-compose up -d --build

destroy:
	docker-compose down -v $(c)

stop:
	docker-compose stop

start:
	docker-compose start

logs:
	docker-compose logs --tail=100

init_db:
	docker exec -it notification-api alembic upgrade head
