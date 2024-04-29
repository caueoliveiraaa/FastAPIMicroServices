run: stop
	docker compose build
	docker compose up -d
	docker compose ps
restart:
	docker compose down -t 0
	docker compose up -d
logs:
	docker compose logs user-api
	docker compose logs order-api
build:
	docker compose build
stop:
	docker compose down -t 0
