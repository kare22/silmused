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

```bash
# Run all integration tests
pytest tests/integration/ -v

# Run specific integration test file
pytest tests/integration/test_runner_integration.py -v

# Run with markers
pytest tests/integration/ -m integration -v
```

## Fixtures

- `mock_postgres_connection`: Mock PostgreSQL connection and cursor
- `temp_sql_file`: Temporary SQL file for testing

## Note

Integration tests use mocks for database operations to avoid requiring a running PostgreSQL instance. For full end-to-end tests with a real database, create separate test files that can be run with a test database.

