# Simple Makefile for common tasks

.PHONY: help setup start clean update

help:
	@echo "Available commands:"
	@echo "  make setup    - Run initial setup"
	@echo "  make start    - Start Jupyter Lab server"
	@echo "  make clean    - Clean temporary files"
	@echo "  make update   - Update dependencies"
	@echo "  make help     - Show this message"

setup:
	python setup.py

start:
	poetry run jupyter lab

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.log" -delete 2>/dev/null || true

update:
	poetry update
