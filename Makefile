.PHONY: help sm mm mi sh test run

help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  sm - Show all migrations"
	@echo "  mm - Make migrations"
	@echo "  mi - Apply migrations"
	@echo "  sh - Open a Django shell"
	@echo "  test - Run tests"
	@echo "  run - Run the development server"

sm:
	uv run python manage.py showmigrations

mm:
	uv run python manage.py makemigrations

mi:
	uv run python manage.py migrate

sh:
	uv run python manage.py shell

test:
	uv run pytest -n auto

run:
	uv run python manage.py runserver