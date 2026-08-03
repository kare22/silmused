# Integration Tests

This directory contains integration tests for the Silmused framework that test multiple components working together.

## Test Coverage

### Runner Integration Tests
- `test_runner_integration.py`: Tests Runner class orchestrating multiple test types
  - Database tests with StructureTest
  - ChecksLayer integration
  - ExecuteLayer integration
  - Query test mode
  - Error handling

### Translator Integration Tests
- `test_translator_integration.py`: Tests Translator with real locale files
  - Locale file loading
  - Complete translation workflows
  - Locale switching
  - All test type translations

## Running Integration Tests

Run these commands from this `automated-tests/integration` directory. Install the test dependencies first if the package is not already installed in the active Python environment:

```bash
python -m pip install -r ../../requirements-dev.txt
```

```bash
# Run all integration tests
python -m pytest . -v

# Run specific integration test file
python -m pytest test_runner_integration.py -v

# Run with markers
python -m pytest . -m integration -v
```

## Fixtures

- `mock_postgres_connection`: Mock PostgreSQL connection and cursor
- `temp_sql_file`: Temporary SQL file for testing

## Note

Integration tests use mocks for database operations to avoid requiring a running PostgreSQL instance. For full end-to-end tests with a real database, create separate test files that can be run with a test database.

