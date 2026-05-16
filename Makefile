.PHONY: install test lint format run clean help

help:
	@echo "Comandos disponibles:"
	@echo "  make install      Instala el paquete en modo editable con deps de dev"
	@echo "  make test         Corre pytest"
	@echo "  make test-fast    Corre pytest excluyendo tests lentos"
	@echo "  make lint         Verifica formato y linting"
	@echo "  make format       Aplica black y ruff fix"
	@echo "  make run          Ejecuta el pipeline end-to-end sobre Lalonde"
	@echo "  make clean        Limpia caches y artefactos"

install:
	pip install -e ".[dev]"
	@echo "Instalación completa. Para benchmarks opcionales: pip install -e '.[dev,benchmark]'"

test:
	pytest

test-fast:
	pytest -m "not slow"

lint:
	ruff check src/ tests/
	black --check src/ tests/

format:
	black src/ tests/
	ruff check --fix src/ tests/

run:
	python -m causal_pipeline.application.lalonde_main

clean:
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .ipynb_checkpoints -exec rm -rf {} +
