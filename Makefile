run:
	@echo "Starting backend"
	PYTHONPATH=./backend/ python -m uvicorn src.main:app --reload --port 8000
