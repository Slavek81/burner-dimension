# Makefile for Gas Burner Calculator

.PHONY: help install clean test lint security ci-local quality-check run docs

# Default target
help:
	@echo "Available targets:"
	@echo "  install       - Install dependencies and setup development environment"
	@echo "  clean         - Clean temporary files and caches"
	@echo "  test-all      - Run all tests with coverage"
	@echo "  lint          - Run code linting with flake8"
	@echo "  security-check- Run security analysis with bandit"
	@echo "  quality-check - Run linting and security checks"
	@echo "  ci-local      - Run complete CI pipeline locally"
	@echo "  run           - Run the main application"
	@echo "  docs          - Generate documentation"

# Install dependencies and setup development environment
install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install pre-commit pytest-cov flake8 bandit black
	pre-commit install
	@echo "Development environment setup complete"

# Clean temporary files and caches
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/
	@echo "Cleaned temporary files"

# Run all tests with coverage
test-all:
	python -m pytest tests/ -v --tb=short
	python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html
	@echo "All tests completed with coverage report"

# Run code linting
lint:
	flake8 src/ gui/ tests/ --max-line-length=100 --exclude=__pycache__
	@echo "Linting completed"

# Run security analysis
security-check:
	bandit -r src/ gui/ --severity-level medium
	@echo "Security check completed"

# Run quality checks (linting + security)
quality-check: lint security-check
	@echo "Quality checks completed"

# Run complete CI pipeline locally (matches GitHub Actions)
ci-local:
	@echo "Running complete CI pipeline locally..."
	@echo "1. Code linting..."
	flake8 src/ gui/ tests/ --max-line-length=100 --exclude=__pycache__
	@echo "2. Security analysis..."
	bandit -r src/ gui/ --severity-level medium
	@echo "3. Running tests..."
	python -m pytest tests/ -v --tb=short
	@echo "4. Coverage analysis..."
	python -m pytest tests/ --cov=src --cov-report=term-missing
	@echo "✅ All CI checks passed!"

# Run the main application
run:
	python main.py

# Generate documentation
docs:
	@echo "Generating documentation..."
	@mkdir -p docs/api
	@echo "Documentation placeholder created"
	@echo "TODO: Add Sphinx documentation generation"

# Development shortcuts
dev-test:
	python -m pytest tests/ -v -x --tb=short

dev-run:
	python main.py

# Format code (optional)
format:
	black src/ gui/ tests/ --line-length=100
	@echo "Code formatting completed"