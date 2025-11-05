- [Silmused Overview](#silmused-overview)
   * [Introduction & Purpose](#introduction-purpose)
      + [What is Silmused?](#what-is-silmused)
      + [Key Use Cases](#key-use-cases)
      + [Current Versions](#current-versions)
   * [Architecture Overview](#architecture-overview)
      + [Core Components](#core-components)
      + [Test Types Categorization](#test-types-categorization)
         - [Database Tests](#database-tests)
         - [Query Tests](#query-tests)
      + [Layer System](#layer-system)
   * [Component Reference](#component-reference)
      + [Runner](#runner)
         - [Initialization Parameters](#initialization-parameters)
         - [Database Creation](#database-creation)
         - [Key Methods](#key-methods)
      + [TestDefinition](#testdefinition)
         - [Common Methods](#common-methods)
         - [Error Handling](#error-handling)
      + [Test Classes](#test-classes)
         - [StructureTest](#structuretest)
         - [DataTest](#datatest)
         - [ConstraintTest](#constrainttest)
         - [FunctionTest](#functiontest)
         - [ProcedureTest](#proceduretest)
         - [ViewTest](#viewtest)
         - [IndexTest](#indextest)
         - [TriggerTest](#triggertest)
         - [QueryStructureTest](#querystructuretest)
         - [QueryDataTest](#querydatatest)
      + [Supporting Classes](#supporting-classes)
         - [ChecksLayer](#checkslayer)
         - [ExecuteLayer](#executelayer)
         - [TitleLayer](#titlelayer)
      + [Translator](#translator)
   * [Test Parameters Reference](#test-parameters-reference)
      + [Parameter Usage Patterns](#parameter-usage-patterns)
         - [String Handling](#string-handling)
         - [Expected Value Patterns](#expected-value-patterns)
         - [Column Name Patterns](#column-name-patterns)
   * [Usage Patterns](#usage-patterns)
      + [Database Testing Workflow](#database-testing-workflow)
      + [Query Testing Workflow](#query-testing-workflow)
      + [Command Line Interface](#command-line-interface)
      + [Complete Example](#complete-example)
   * [Output Format](#output-format)
      + [JSON Structure](#json-structure)
      + [Points Calculation](#points-calculation)
      + [Feedback System](#feedback-system)
      + [Result Structure](#result-structure)
   * [Translation System](#translation-system)
      + [Overview](#overview)
      + [Translation File Structure](#translation-file-structure)
      + [Supported Languages](#supported-languages)
      + [Test Types and Keys](#test-types-and-keys)
      + [Message Templates](#message-templates)
      + [Usage](#usage)
      + [Custom Feedback](#custom-feedback)
   * [Best Practices](#best-practices)
   * [Troubleshooting](#troubleshooting)
      + [Common Issues](#common-issues)
   * [Additional Resources](#additional-resources)

# Silmused Overview

A comprehensive guide to the Silmused PostgreSQL testing framework.

## Introduction & Purpose

### What is Silmused?

Silmused is a Python-based testing framework designed to automatically validate PostgreSQL databases and SQL queries. It provides a comprehensive suite of test classes that can verify database structures, data integrity, constraints, functions, procedures, triggers, views, indexes, and query results.

### Key Use Cases

Silmused supports two main testing modes:

1. **Database Tests** - Validates the structure and content of a PostgreSQL database:
   - Table and view structure (columns, types, constraints)
   - Data content and correctness
   - Constraints (primary keys, foreign keys, unique, check)
   - Functions and procedures
   - Triggers
   - Indexes

2. **Query Tests** - Validates SQL query results:
   - Query structure (columns present/absent)
   - Query data (row counts, specific values, value ranges)
   - Result ordering (using `test_id` column)

### Current Versions

- Python: 3.12
- psycopg2: 2.9.9
- Silmused: 1.4.6

## Architecture Overview

### Core Components

Silmused is built around three main components:

1. **Runner** - The orchestration engine that:
   - Creates temporary test databases
   - Executes test suites
   - Formats results into JSON output
   - Manages database connections

2. **TestDefinition** - The base class for all test types that:
   - Provides common parameters and behavior
   - Handles error catching and feedback generation
   - Manages test execution lifecycle

3. **Translator** - The internationalization system that:
   - Provides multi-language feedback messages
   - Supports template-based message formatting
   - Currently supports English and Estonian

### Test Types Categorization

#### Database Tests

These test classes inherit from `TestDefinition` and validate database structures:

- `StructureTest` - Tests table/view structure
- `DataTest` - Tests table/view data content
- `ConstraintTest` - Tests table/column constraints
- `FunctionTest` - Tests database functions
- `ProcedureTest` - Tests stored procedures
- `ViewTest` - Tests views and materialized views
- `IndexTest` - Tests database indexes
- `TriggerTest` - Tests database triggers

#### Query Tests

These test classes validate SQL query results:

- `QueryStructureTest` - Tests query result structure (columns)
- `QueryDataTest` - Tests query result data

**Important:** Query tests use a special workflow where the input SQL query is executed and results are stored in a temporary table named `query_test` with an additional `test_id` column for row ordering.

### Layer System

Three supporting classes provide organizational and execution capabilities:

1. **ChecksLayer** - Groups related tests together with a shared title
2. **ExecuteLayer** - Executes SQL queries between tests (useful for trigger testing)
3. **TitleLayer** - Adds section titles to test output

These classes do not inherit from `TestDefinition` as they serve organizational purposes rather than testing functionality.

## Component Reference

### Runner

The `Runner` class is the primary interface for executing tests. It handles database creation, test execution, and result formatting.

#### Initialization Parameters

```python
Runner(
    backup_file_path,      # Required: Path to SQL dump or SQL script
    tests,                 # Required: List of test objects
    lang='en',             # Language for feedback ('en' or 'et')
    test_name='',          # Optional name for test database
    db_user='postgres',    # PostgreSQL username
    db_host='localhost',   # Database host
    db_password='postgres', # Database password
    db_port='5432',        # Database port
    test_query='test',      # 'test' for database tests, 'query' for query tests
    query_sql='',          # SQL query string (for query tests)
    encoding=None          # File encoding (e.g., 'UTF-8')
)
```

#### Database Creation

The Runner automatically:
1. Creates a randomly-named database (format: `db_{test_name}_{filename}_{uuid}`)
2. Accepts both `pg_dump` binary files and SQL scripts (INSERT statements)
3. Validates file format before processing
4. Handles encoding issues (including PostgreSQL 17.6+ `\restrict` commands)

#### Key Methods

- `get_results()` - Returns JSON-formatted test results in OK_V3 format
- `_run_tests()` - Executes all tests in sequence
- `_create_db_from_psql_dump()` - Creates database from pg_dump file
- `_create_db_from_psql_insert()` - Creates database from SQL script
- `_create_query_view()` - Creates temporary query_test table for query tests

### TestDefinition

The base class for all test types (except Layers). Provides common functionality:

#### Common Methods

- `run(cursor)` - Main entry point that executes the test and handles errors
- `execute(cursor)` - Abstract method implemented by each test class
- `response(is_success, message_success, message_failure, points, is_sys_fail)` - Formats test response

#### Error Handling

TestDefinition automatically handles common SQL errors:
- `UndefinedColumn` - Column doesn't exist
- `UndefinedTable` - Table doesn't exist
- `AmbiguousColumn` - Column reference is ambiguous
- `UndefinedFunction` - Function doesn't exist
- `IndexError` - No result found

These errors are caught and formatted into user-friendly feedback messages.

### Test Classes

#### StructureTest

Tests table/view structure using `information_schema.columns`.

**Key Features:**
- Tests table/view existence
- Tests column existence
- Tests column data types
- Tests column maximum length (for varchar)

**Supported Types:**
- `'integer'` - Matches: tinyint, smallint, mediumint, int, bigint, integer
- `'float'` - Matches: float, double, decimal
- `'varchar'` - Matches: character varying
- `'text'` - Matches: text
- `'boolean'` - Matches: boolean

#### DataTest

Tests table/view data content using direct SQL queries.

**Key Features:**
- Tests data existence
- Tests exact values
- Tests value ranges (for numbers)
- Tests value lists (for strings)
- Tests NULL values
- Supports WHERE clauses
- Supports JOIN clauses (INNER JOIN)

#### ConstraintTest

Tests table/column constraints using `information_schema.table_constraints` and `information_schema.key_column_usage`.

**Key Features:**
- Tests constraint existence
- Tests constraint types (PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK)
- Tests constraint names
- Tests multi-column constraints

#### FunctionTest

Tests database functions using `pg_catalog.pg_proc` and `information_schema.routines`.

**Key Features:**
- Tests function existence
- Tests function type (FUNCTION vs PROCEDURE)
- Tests function parameter count
- Tests function return values
- Tests function result count
- Supports function arguments

#### ProcedureTest

Tests stored procedures using similar approach to FunctionTest.

**Key Features:**
- Tests procedure existence
- Tests procedure type
- Tests procedure parameter count
- Tests procedure result count via `after_query`
- Supports `pre_query` for setup
- Requires `after_query` to verify results

#### ViewTest

Tests views using `information_schema.columns` and `pg_matviews`.

**Key Features:**
- Tests view existence
- Tests view columns
- Tests materialized views (via `isMaterialized=True`)

#### IndexTest

Tests database indexes using `pg_indexes`.

**Key Features:**
- Tests index existence by name

#### TriggerTest

Tests database triggers using `information_schema.triggers`.

**Key Features:**
- Tests trigger existence
- Tests trigger event manipulation (INSERT, UPDATE, DELETE)
- Tests trigger action timing (BEFORE, AFTER)
- Often used with `ExecuteLayer` for setup

#### QueryStructureTest

Tests query result structure (columns) using `information_schema.columns` on the `query_test` table.

**Key Features:**
- Tests column existence in query results
- Tests column absence (via `should_exist=False`)

#### QueryDataTest

Tests query result data using direct SQL queries on the `query_test` table.

**Key Features:**
- Tests row counts
- Tests specific values (using `test_id` for row ordering)
- Tests value ranges
- Tests value lists
- Supports WHERE clauses

### Supporting Classes

#### ChecksLayer

Groups related tests together with a shared title. Results are nested in the output JSON.

**Parameters:**
- `title` - Title for the test group
- `tests` - List of test objects

**Example:**
```python
ChecksLayer(
    title='Users table validation',
    tests=[
        StructureTest(name='users', points=10),
        DataTest(name='users', column_name='COUNT(*)', expected_value=100, points=20)
    ]
)
```

#### ExecuteLayer

Executes SQL queries between tests. Useful for preparing data before trigger tests.

**Parameters:**
- `query` - SQL query to execute

**Example:**
```python
ExecuteLayer("INSERT INTO users (email) VALUES ('test@example.com')")
```

#### TitleLayer

Adds section titles to test output. Appears as a message in results.

**Parameters:**
- `title` - Title string

**Example:**
```python
TitleLayer('Database Structure Tests')
```

### Translator

The Translator class provides internationalization support for feedback messages.

**Features:**
- Loads translation files from `silmused/locale/`
- Supports JSON-based translation files
- Template-based message formatting with parameter substitution
- Currently supports: English (`en.json`) and Estonian (`et.json`)

**Translation Structure:**
- Organized by test type (e.g., `structure_test`, `data_test`)
- Each test type has test keys (e.g., `table_should_exist_positive_feedback`)
- Messages support up to 5 parameters (`$param1` through `$param5`)

## Test Parameters Reference

All test classes inherit common parameters from `TestDefinition`. The following table describes all available parameters:

| Parameter | Type | Default | Required | Description |
|-----------|------|---------|----------|-------------|
| `name` | string | - | **Yes** | Table/view/function/procedure/trigger/index name (must be lowercase, cannot be empty) |
| `points` | int/float | `0` | No | Points awarded for this test |
| `title` | string | `None` | No | Test description shown in feedback |
| `column_name` | string/list | `None` | No | Column name(s) to test (must be lowercase; can be string or list for multiple columns) |
| `should_exist` | boolean | `True` | No | Whether result should exist (`True`) or not exist (`False`) |
| `expected_value` | any | `None` | No | Expected value; can be: single value, `'NULL'`, or list `[min, max]` for numeric range, or list of strings for value matching |
| `where` | string | `None` | No | WHERE clause for filtering (SQL values use single quotes inside Python double quotes) |
| `join` | string | `None` | No | JOIN clause (currently only INNER JOIN supported) |
| `description` | string | `None` | No | Internal description (not displayed in feedback, only visible to test writer) |
| `arguments` | list | `None` | No | Function/procedure arguments, or info_schema column selection |
| `expected_type` | string | `None` | No | Expected column type (`'varchar'`, `'integer'`, `'decimal'`, `'float'`, `'text'`, `'boolean'`) |
| `expected_character_maximum_length` | int | `None` | No | Expected column maximum length (for varchar types) |
| `expected_count` | int/list | `None` | No | Expected row count (for functions/procedures); can be integer or list for range |
| `pre_query` | string | `None` | No | SQL to run before test (procedure tests only) |
| `after_query` | string | `None` | No | SQL to run after test (required for procedure tests) |
| `custom_feedback` | string | `None` | No | Custom feedback message (overwrites default translated feedback) |
| `query` | string | `None` | No | **Should not be used** - automatically generated by test classes |
| `constraint_name` | string | `None` | No | Constraint name (ConstraintTest only) |
| `constraint_type` | string | `None` | No | Constraint type: `'PRIMARY KEY'`, `'FOREIGN KEY'`, `'UNIQUE'`, `'CHECK'` (ConstraintTest only) |
| `number_of_parameters` | int | `None` | No | Expected number of function/procedure parameters (FunctionTest/ProcedureTest only) |
| `isMaterialized` | boolean | `False` | No | Whether view is materialized (ViewTest only) |
| `action_timing` | string | `None` | No | Trigger action timing: `'BEFORE'` or `'AFTER'` (TriggerTest only) |

### Parameter Usage Patterns

#### String Handling

When writing WHERE clauses, remember:
- SQL values must be in single quotes: `'value'`
- Python strings use double quotes: `"..."`

**Example:**
```python
DataTest(
    name='users',
    where="email='admin@example.com'",  # SQL uses ' inside Python "
    points=15
)
```

**For columns with spaces or special characters:**
```python
QueryDataTest(
    name='query_test',
    where='"Title beginning"' + "='Dance'",  # Column name with spaces
    points=20
)
```

#### Expected Value Patterns

**Single Value:**
```python
expected_value=100
expected_value='admin@example.com'
expected_value='NULL'
```

**Numeric Range:**
```python
expected_value=[100, 200]  # Value must be between 100 and 200
```

**String List:**
```python
expected_value=['active', 'pending', 'inactive']  # Value must be in this list
```

#### Column Name Patterns

**Single Column:**
```python
column_name='email'
```

**Multiple Columns:**
```python
column_name=['email', 'username']  # Tests for multiple columns
```

## Usage Patterns

### Database Testing Workflow

1. **Prepare Database:**
   ```bash
   pg_dump -U postgres mydatabase > mydb.sql
   ```

2. **Write Tests:**
   ```python
   from silmused import Runner, ChecksLayer, StructureTest, DataTest, ConstraintTest, TitleLayer

   tests = [
       TitleLayer('Table Structure'),
       ChecksLayer(
           title='Users table',
           tests=[
               StructureTest(name='users', title='Table exists', points=10),
               StructureTest(name='users', column_name='email', expected_type='varchar', points=15),
               ConstraintTest(name='users', constraint_type='PRIMARY KEY', points=20),
               DataTest(name='users', column_name='COUNT(*)', expected_value=100, points=25)
           ]
       )
   ]
   ```

3. **Run Tests:**
   ```python
   runner = Runner(
       backup_file_path='mydb.sql',
       tests=tests,
       lang='en'
   )
   results = runner.get_results()
   print(results)
   ```

### Query Testing Workflow

1. **Prepare Database and Query:**
   - Database SQL file (for query execution context)
   - SQL query file (the query to test)

2. **Write Query Tests:**
   ```python
   from silmused import Runner, QueryStructureTest, QueryDataTest

   tests = [
       QueryStructureTest(
           name='query_test',  # Always 'query_test' for query tests
           column_name='Title',
           title='Query has Title column',
           points=20
       ),
       QueryDataTest(
           name='query_test',
           column_name='COUNT(*)',
           expected_value=10,
           title='Query returns 10 rows',
           points=30
       ),
       QueryDataTest(
           name='query_test',
           column_name='pealkiri',
           where="test_id=1",  # test_id is added automatically for row ordering
           expected_value="Madness of Love",
           title='First row is correct',
           points=30
       )
   ]
   ```

3. **Run Query Tests:**
   ```python
   with open('query.sql', 'r') as f:
       query_sql = f.read()

   runner = Runner(
       backup_file_path='database.sql',
       tests=tests,
       test_query='query',  # Enable query test mode
       query_sql=query_sql,
       lang='en'
   )
   results = runner.get_results()
   print(results)
   ```

### Command Line Interface

Silmused can be run from the command line:

**Database Tests:**
```bash
silmused <database_dump_file> <tests_file> <db_user> <hostname> <port> <db_password> <test_language> test '' <encoding>
```

**Example:**
```bash
silmused lahendus.sql tests.py postgres localhost 5432 postgresql en test '' UTF-8
```

**Query Tests:**
```bash
silmused <query_file> <tests_file> <db_user> <hostname> <port> <db_password> <test_language> query <query_test_database> <encoding>
```

**Example:**
```bash
silmused query.sql euro_kodu_3_2.py postgres localhost 5432 postgresql et query eurovisioon.sql UTF-8
```

**Note:** The tests file must include an array with the key `"tests"`:
```python
tests = [
    StructureTest(...),
    DataTest(...)
]
```

### Complete Example

```python
from silmused import (
    Runner, ChecksLayer, StructureTest, DataTest, 
    ConstraintTest, FunctionTest, TitleLayer
)

tests = [
    TitleLayer('Database Structure'),
    
    ChecksLayer(
        title='Users table validation',
        tests=[
            StructureTest(name='users', title='Table exists', points=10),
            StructureTest(name='users', column_name='email', expected_type='varchar', expected_character_maximum_length=255, points=15),
            StructureTest(name='users', column_name='created_at', expected_type='timestamp', points=10),
            ConstraintTest(name='users', constraint_type='PRIMARY KEY', points=20),
            ConstraintTest(name='users', constraint_type='UNIQUE', column_name='email', points=15),
            DataTest(name='users', column_name='COUNT(*)', expected_value=100, points=20),
            DataTest(name='users', where="email='admin@example.com'", expected_value='admin@example.com', column_name='email', points=10)
        ]
    ),
    
    TitleLayer('Functions'),
    
    FunctionTest(
        name='calculate_total',
        arguments=[100, 0.2],
        expected_value=120,
        number_of_parameters=2,
        title='Calculate total function works correctly',
        points=30
    )
]

runner = Runner(
    backup_file_path='database.sql',
    tests=tests,
    lang='en',
    encoding='UTF-8'
)

results = runner.get_results()
print(results)
```

## Output Format

### JSON Structure

Results are returned as JSON in OK_V3 format:

```json
{
  "result_type": "OK_V3",
  "points": 85,
  "producer": "silmused 1.4.5",
  "finished_at": "2024-01-15T10:30:00Z",
  "tests": [
    {
      "title": "Users table exists",
      "status": "PASS",
      "feedback": ""
    },
    {
      "title": "Email column exists",
      "status": "FAIL",
      "feedback": "Wrong, expected to find column email in table users"
    },
    {
      "title": "Users table validation",
      "status": "FAIL",
      "checks": [
        {
          "title": "Table exists",
          "status": "PASS",
          "feedback": ""
        },
        {
          "title": "Email column exists",
          "status": "FAIL",
          "feedback": "Wrong, expected to find column email in table users"
        }
      ]
    }
  ]
}
```

### Points Calculation

- Points are calculated as: `(earned_points / total_points) * 100`
- If all tests have 0 points, the system treats it as a pass/fail test (100% if all pass, 0% if any fail)
- Final score is rounded to nearest integer

### Feedback System

Feedback messages are generated through the Translator system:
1. Test execution determines success/failure
2. Test type and test key are determined
3. Translator looks up message in locale file
4. Parameters are substituted into message template
5. Custom feedback (if provided) overrides default messages

### Result Structure

- **Root Level:**
  - `result_type`: Always `"OK_V3"`
  - `points`: Percentage score (0-100)
  - `producer`: Version string (e.g., `"silmused 1.4.5"`)
  - `finished_at`: ISO 8601 timestamp
  - `tests`: Array of test results

- **Test Result:**
  - `title`: Test title
  - `status`: `"PASS"` or `"FAIL"`
  - `feedback`: Human-readable feedback message (empty for passing tests)
  - `checks`: (Optional) Nested results for ChecksLayer groups

- **System Failures:**
  - `exception_message`: Raw exception message for system failures
  - `status`: `"FAIL"` for system failures

## Translation System

### Overview

Silmused uses a JSON-based translation system located in `silmused/locale/`. Translation files are organized by test type and test key.

### Translation File Structure

```json
{
  "test_type": {
    "test_key": "Message template with $param1, $param2, etc.",
    ...
  },
  ...
}
```

### Supported Languages

- **English** (`en`) - Default, located in `silmused/locale/en.json`
- **Estonian** (`et`) - Located in `silmused/locale/et.json`

### Test Types and Keys

Translation messages are organized by test type:

- `structure_test` - StructureTest messages
- `data_test` - DataTest messages
- `constraint_test` - ConstraintTest messages
- `function_test` - FunctionTest messages
- `procedure_test` - ProcedureTest messages
- `view_test` - ViewTest messages
- `index_test` - IndexTest messages
- `trigger_test` - TriggerTest messages
- `query_structure_test` - QueryStructureTest messages
- `query_data_test` - QueryDataTest messages
- `sys_fail` - System error messages

### Message Templates

Messages support parameter substitution using `$param1` through `$param5`:

**Example:**
```json
{
  "structure_test": {
    "table_should_exist_positive_feedback": "Correct, table $param1 was found",
    "table_should_exist_negative_feedback": "Wrong, expected to find table $param1, but none were found"
  }
}
```

### Usage

Set the language when creating the Runner:

```python
runner = Runner(
    backup_file_path='database.sql',
    tests=tests,
    lang='et'  # Estonian feedback
)
```

### Custom Feedback

Every test supports `custom_feedback` parameter that overrides the default translated messages:

```python
DataTest(
    name='users',
    column_name='COUNT(*)',
    expected_value=100,
    custom_feedback='Expected exactly 100 users, but found a different number',
    points=20
)
```

When `custom_feedback` is provided, it replaces both positive and negative feedback messages.

## Best Practices

1. **Always use lowercase for table/column names** - Silmused expects lowercase names
2. **Use descriptive titles** - They appear in test results and help debugging
3. **Group related tests** - Use `ChecksLayer` to organize tests logically
4. **Set appropriate points** - Total points typically sum to 100 for percentage scoring
5. **Use `description` for internal notes** - Not shown in feedback, useful for documentation
6. **Test incrementally** - Start with structure tests, then data tests
7. **Handle edge cases** - Test both positive (`should_exist=True`) and negative (`should_exist=False`) cases
8. **Use string concatenation for complex WHERE clauses** - When dealing with column names containing spaces or special characters
9. **For query tests, always use `name='query_test'`** - This is the automatically created table name
10. **Use `test_id` for row ordering in query tests** - The `test_id` column is automatically added for row ordering

## Troubleshooting

### Common Issues

**Problem:** Tests fail with "table not found"
- **Solution:** Ensure table names are lowercase in tests

**Problem:** Query tests not working
- **Solution:** Make sure `test_query='query'` and `query_sql` is set, and use `name='query_test'` for all query tests

**Problem:** Encoding errors
- **Solution:** Specify `encoding='UTF-8'` when loading SQL files with special characters

**Problem:** Database connection fails
- **Solution:** Check database credentials, host, port, and ensure PostgreSQL is running

**Problem:** Expected value not matching
- **Solution:** Check data types - use string conversion for comparisons if needed

**Problem:** Procedure tests fail
- **Solution:** Ensure `after_query` is provided (required for procedure tests)

**Problem:** Constraint tests not finding constraints
- **Solution:** Check constraint names and types - they must match exactly (case-sensitive)

## Additional Resources

- Check `silmused/test_cases/` for example test files
- Review `demo.py` and `query_demo.py` for complete working examples

