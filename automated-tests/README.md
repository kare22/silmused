# Automated Tests

This directory contains the automated tests for Silmused. Tests are grouped into fast core unit tests, feedback message tests, and mocked integration tests.

## Setup

Install the package and test dependencies from the repository root:

```bash
python -m pip install -r requirements-dev.txt
```

## Running Tests

Run these commands from the repository root.

Run the full suite:

```bash
python -m pytest automated-tests
```

Run focused suites:

```bash
python -m pytest automated-tests/test_core
python -m pytest automated-tests/test_feedback
python -m pytest automated-tests/integration
```

Pytest markers are applied automatically based on the test directory:

```bash
python -m pytest -m core
python -m pytest -m feedback
python -m pytest -m integration
```

## Layout

- `test_core/` - Unit tests for core framework classes and helpers.
- `test_feedback/` - Feedback message tests for each test type.
- `integration/` - Mocked integration tests for component workflows.

Integration tests currently mock PostgreSQL connections and do not require a running database.
