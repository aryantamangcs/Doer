run:
	@echo "Starting backend"
	uvicorn backend.src.main:app --reload --port 8000
