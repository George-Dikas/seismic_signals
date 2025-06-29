local:
	docker-compose -f docker-compose.yml down && docker-compose -f docker-compose.yml up --build

watch:
	docker-compose -f docker-compose.yml down && docker-compose -f docker-compose.yml up --build --watch

prune:
	docker-compose -f docker-compose.yml down --rmi local -v

stop:
	docker-compose -f docker-compose.yml down