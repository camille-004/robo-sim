SRC = robo_sim/ tests/ setup.py

.PHONY: help format lint all

format:
	black --line-length 80 $(SRC)
	isort $(SRC) --multi-line=3 --trailing-comma --force-grid-wrap=0 --line-length=80 --use-parentheses

lint:
	flake8 $(SRC)

all: format lint

help:
	@echo "Available commands:"
	@echo "  format - Format code with black."
	@echo "  lint   - Lint code with flake8."
	@echo "  all    - Run both 'format' and 'lint'."