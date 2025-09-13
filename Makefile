run:
	@echo "Starting backend"
	PYTHONPATH=./backend/ python -m uvicorn src.main:app --reload --port 8080
migration:
	@echo "Creating migration"
	PYTHONPATH=./backend/ MIGRATION_NAME=$(name) alembic -c ./backend/alembic.ini revision -m "$(msg)" --rev-id $(shell date -u +%Y%m%d_%H%M%S)
migrate:
	@echo "Migrating the migrations to the database"
	PYTHONPATH=./backend/ alembic -c ./backend/alembic.ini upgrade head
downgrade:
	@echo "Migrating the migrations to the database"
	alembic downgrade -1
