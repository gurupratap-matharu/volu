APP_LIST ?= main pages users blog places 
.PHONY: collectstatic run test ci install install-dev migrations staticfiles

help:
	@echo "Available commands"
	@echo " - ci               : lints, migrations, tests, coverage"
	@echo " - install          : installs production requirements"
	@echo " - install-dev      : installs development requirements"
	@echo " - isort            : sorts all imports of the project"
	@echo " - lint             : lints the codebase"
	@echo " - run              : runs the development server"
	@echo " - setup-test-data  : erases the db and loads mock data"
	@echo " - shellplus        : runs the development shell"

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

clean:
	docker-compose exec web rm -rf __pycache__ .pytest_cache
	rm -rf __pycache__ .pytest_cache

check:
	docker-compose exec web python manage.py check

check-deploy:
	docker-compose exec web python manage.py check --deploy

up:
	docker-compose up -d --build

down:
	docker-compose down

ps:
	docker-compose ps
	
logs:
	docker-compose logs -f

build:down up ps

buildlogs:build logs

shellplus:
	docker-compose exec web python manage.py shell_plus

shell:
	docker-compose exec web python manage.py shell

showmigrations:
	docker-compose exec web python manage.py showmigrations

makemigrations:
	docker-compose exec web python manage.py makemigrations

migrate:
	docker-compose exec web python manage.py migrate

migrations-check:
	docker-compose exec web python manage.py makemigrations --check --dry-run

isort:
	isort $(APP_LIST)

lint: isort
	flake8 $(APP_LIST)

test: migrations-check
	docker-compose exec web python manage.py test -v 2

ci: lint test
	python manage.py coverage report

ci: test