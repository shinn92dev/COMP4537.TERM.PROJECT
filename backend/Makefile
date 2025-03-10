PORT=8000
HOST=0.0.0.0
APP=main:app

# This would work only for window

run:
	@echo "🚀 Starting FastAPI server at http://localhost:$(PORT) 🚀"
	cmd /k "venv\Scripts\activate.bat && python -m uvicorn $(APP) --host $(HOST) --port $(PORT) --reload"

venv: FORCE
	cmd /k "venv\Scripts\activate.bat"

FORCE:

install:
	pip install --upgrade pip
	pip install -r requirements.txt

save-lib:
	pip freeze > requirements.txt