install:
	brew install poetry
	poetry install

run:
	poetry run python main.py --days-ahead=6
