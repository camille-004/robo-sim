SRC = robo_sim/ tests/ docs/ setup.py

.PHONY: help format lint all

format:
	black --line-length 79 $(SRC)
	isort $(SRC) --multi-line=3 --trailing-comma --force-grid-wrap=0 --line-length=80 --use-parentheses

lint:
	flake8 $(SRC)

test:
	pytest tests/

all: format lint test

help:
	@echo "Available commands:"
	@echo "  format - Format code with black."
	@echo "  lint   - Lint code with flake8."
	@echo "  test   - Run unit tests with pytest."
	@echo "  all    - Run both 'format', 'lint', and 'test'."