# Code Quality Tests

This directory contains code quality checks and tests for the Silmused framework.

## Tools Used

- **Ruff**: Fast Python linter
- **Black**: Code formatter
- **MyPy**: Static type checker
- **Pytest-cov**: Code coverage

## Running Code Quality Checks

### Linting (Ruff)
```bash
ruff check silmused/
ruff format silmused/  # Auto-fix issues
```

### Formatting (Black)
```bash
black silmused/  # Format code
black --check silmused/  # Check formatting
```

### Type Checking (MyPy)
```bash
mypy silmused/ --ignore-missing-imports
```

### All Checks
```bash
# Run all code quality tests
pytest tests/code_quality/ -v

# Or run checks manually
ruff check silmused/
black --check silmused/
mypy silmused/ --ignore-missing-imports
```

## Configuration

Configuration files:
- `pyproject.toml` - Configuration for all tools
- `pytest.ini` - Pytest configuration

## Integration with CI/CD

These checks should be run in CI/CD pipelines to ensure code quality before merging.

