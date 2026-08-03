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
         - [Dynamic Expected Values](#dynamic-expected-values)
         - [Alternative Column Names](#alternative-column-names)
         - [Elements Checks](#elements-checks)
         - [Debug Mode](#debug-mode)
         - [LLM Check](#llm-check)
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
   * [Development & Test Suite](#development-test-suite)
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
- Silmused: 1.7.8

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
- Tests column existence, including multiple columns
- Tests column data types
- Tests column maximum length (for varchar)
- Supports `debug` and `llm_check`

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
- Tests dynamically computed expected values with `expected_value_query`
- Tests value ranges (for numbers)
- Tests value lists (for strings)
- Tests NULL values
- Supports WHERE clauses
- Supports JOIN clauses (INNER JOIN)
- Supports view-specific feedback with `isView=True`
- Supports alternative column lookup with `column_name_fallback`
- Supports `debug` and `llm_check`

**Note:** `DataTest.column_name` must be a string. List-based `column_name` checks are supported by structure-oriented tests such as `StructureTest`, `ViewTest`, and `QueryStructureTest`.

#### ConstraintTest

Tests table/column constraints using `information_schema.table_constraints` and `information_schema.key_column_usage`.

**Key Features:**
- Tests constraint existence
- Tests constraint types (PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK)
- Tests constraint names
- Tests multi-column constraints
- Supports `debug` and `llm_check`

#### FunctionTest

Tests database functions using `pg_catalog.pg_proc` and `information_schema.routines`.

**Key Features:**
- Tests function existence
- Tests function type (FUNCTION vs PROCEDURE)
- Tests function parameter count
- Tests function return values
- Tests function result count
- Supports function arguments
- Supports dynamically computed expected values with `expected_value_query`
- Supports required/banned function body elements with `elements`
- Supports result count ranges when `expected_count` is a numeric list
- Supports `debug` and `llm_check`

#### ProcedureTest

Tests stored procedures using similar approach to FunctionTest.

**Key Features:**
- Tests procedure existence
- Tests procedure type
- Tests procedure parameter count
- Tests procedure result count via `after_query`
- Supports `pre_query` for setup
- Requires `after_query` to verify results
- Supports required/banned procedure body elements with `elements`
- Supports `debug` and `llm_check`

**Note:** `after_query` is required for normal procedure result verification. When using `elements`, the test checks procedure source text in `pg_proc.prosrc` rather than executing the procedure result path.

#### ViewTest

Tests views using `information_schema.columns` and `pg_matviews`.

**Key Features:**
- Tests view existence
- Tests view columns, including multiple columns
- Tests materialized views (via `isMaterialized=True`)
- Tests materialized view columns
- Supports required/banned view definition elements with `elements`
- Supports `debug` and `llm_check`

#### IndexTest

Tests database indexes using `pg_indexes`.

**Key Features:**
- Tests index existence by name
- Supports `debug`

#### TriggerTest

Tests database triggers using `information_schema.triggers`.

**Key Features:**
- Tests trigger existence
- Tests trigger event manipulation (INSERT, UPDATE, DELETE)
- Tests trigger action timing (BEFORE, AFTER)
- Often used with `ExecuteLayer` for setup
- Supports `debug` and `llm_check`

#### QueryStructureTest

Tests query result structure (columns) using `information_schema.columns` on the `query_test` table.

**Key Features:**
- Tests column existence in query results
- Tests column absence (via `should_exist=False`)
- Tests required/banned SQL elements in the submitted query with `elements`
- Supports multiple-column checks
- Supports `debug` and `llm_check`

#### QueryDataTest

Tests query result data using direct SQL queries on the `query_test` table.

**Key Features:**
- Tests row counts
- Tests specific values (using `test_id` for row ordering)
- Tests dynamically computed expected values with `expected_value_query`
- Tests value ranges
- Tests value lists
- Supports WHERE clauses
- Supports alternative column lookup with `column_name_fallback`
- Supports `debug` and `llm_check`

**Note:** `QueryDataTest.column_name` must be a string.

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
- `debug` - Optional debug flag. When set, prints the executed query or system error details.

**Example:**
```python
ExecuteLayer("INSERT INTO users (email) VALUES ('test@example.com')", debug='DEBUG')
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
- Messages support positional parameters (`$param1`, `$param2`, etc.) and, for some test types, named placeholders such as `$index_name`, `$trigger_name`, and `$procedure_name`

## Test Parameters Reference

All test classes inherit common parameters from `TestDefinition`. The following table describes all available parameters:

| Parameter                           | Type        | Default | Required | Applies to | Description |
|-------------------------------------|-------------|---------|----------|------------|-------------|
| `name`                              | string      | -       | **Yes** | All tests | Table/view/function/procedure/trigger/index name. Use lowercase names unless the underlying SQL object was created with quoted case-sensitive identifiers. |
| `points`                            | int/float   | `0`     | No | All tests | Points awarded for this test. |
| `title`                             | string      | `None`  | No | All tests | Test description shown in feedback. |
| `column_name`                       | string/list | `None`  | No | Varies by test | Column name(s) to test. `DataTest` and `QueryDataTest` accept a string only; `StructureTest`, `ViewTest`, and `QueryStructureTest` also accept lists. |
| `should_exist`                      | boolean     | `True`  | No | Most tests | Whether the tested result should exist. For `elements`, `True` means required elements and `False` means banned elements. |
| `expected_value`                    | any         | `None`  | No | Data/query/function/view tests | Expected value; can be a single value, `'NULL'`, numeric range/list, or list of strings depending on the test type. |
| `expected_value_query`              | string      | `None`  | No | `DataTest`, `QueryDataTest`, `FunctionTest` | SQL query executed before the assertion; the first result cell becomes `expected_value`. |
| `where`                             | string      | `None`  | No | Data/query/function/structure/view tests | WHERE clause for filtering. SQL values use single quotes inside Python double quotes. |
| `join`                              | string      | `None`  | No | `DataTest`, `QueryDataTest` | JOIN clause. Currently one direct JOIN clause is supported. |
| `description`                       | string      | `None`  | No | All tests | Internal description; included in raw test response but not shown in final feedback. |
| `arguments`                         | list        | `None`  | No | Function/procedure/trigger tests, info_schema selection | Function/procedure arguments, trigger event manipulations, or selected information schema columns. |
| `expected_type`                     | string      | `None`  | No | `StructureTest` | Expected column type: `'varchar'`, `'integer'`, `'float'`, `'text'`, or `'boolean'`. |
| `expected_character_maximum_length` | int         | `None`  | No | `StructureTest` | Expected column maximum length for varchar columns. |
| `expected_count`                    | int/list    | `None`  | No | `FunctionTest`, `ProcedureTest` | Expected row count. Numeric list/range behavior is implemented for `FunctionTest`; `ProcedureTest` uses exact count comparison. |
| `pre_query`                         | string      | `None`  | No | `ProcedureTest` | SQL to run before the procedure call. |
| `after_query`                       | string      | `None`  | **Yes** for `ProcedureTest` | `ProcedureTest` | SQL to run after the procedure call to verify results. |
| `custom_feedback`                   | string      | `None`  | No | Most tests | Custom feedback message. It is routed through the translation system and overrides default positive and negative feedback. |
| `query`                             | string      | `None`  | No | Internal | **Do not set manually** in normal tests; generated by test classes. |
| `constraint_name`                   | string      | `None`  | No | `ConstraintTest` | Constraint name. |
| `constraint_type`                   | string      | `None`  | No | `ConstraintTest` | Constraint type: `'PRIMARY KEY'`, `'FOREIGN KEY'`, `'UNIQUE'`, or `'CHECK'`. |
| `number_of_parameters`              | int         | `None`  | No | `FunctionTest`, `ProcedureTest` | Expected number of function/procedure parameters. |
| `isMaterialized`                    | boolean     | `False` | No | `ViewTest` | Whether the target view is materialized. Supports existence and column checks. |
| `isView`                            | boolean     | `False` | No | `DataTest` | Uses view-specific feedback wording for data tests against views. |
| `action_timing`                     | string      | `None`  | No | `TriggerTest` | Trigger action timing: `'BEFORE'` or `'AFTER'`. |
| `elements`                          | str/list    | `None`  | No | `QueryStructureTest`, `ViewTest`, `FunctionTest`, `ProcedureTest` | Required or banned SQL/source fragments. Controlled by `should_exist`. |
| `column_name_fallback`              | list        | `None`  | No | `DataTest`, `QueryDataTest` | Alternative column name patterns checked with `ILIKE`; the first matching column is used. |
| `llm_check`                         | boolean     | `False` | No | Most `TestDefinition` tests | Pre-runs the generated query and fails if row existence contradicts `should_exist`. |
| `debug`                             | string      | `None`  | No | Most tests, `ExecuteLayer` | Enables debug print output. Valid values are `'DEBUG'` and `'ALL'`. |

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

Multiple-column checks are intended for structure-style tests such as `StructureTest`, `ViewTest`, and `QueryStructureTest`. `DataTest` and `QueryDataTest` require `column_name` to be a single string.

#### Dynamic Expected Values

Use `expected_value_query` when the expected value should be computed from the database at runtime. The first cell of the query result becomes `expected_value`.

```python
DataTest(
    name='orders',
    column_name='COUNT(*)',
    expected_value_query='SELECT COUNT(*) FROM expected_orders',
    points=20
)
```

This is supported by `DataTest`, `QueryDataTest`, and `FunctionTest`.

#### Alternative Column Names

Use `column_name_fallback` when student queries may use acceptable alternative column names. Silmused checks the fallback list with `ILIKE` and uses the first matching column.

```python
QueryDataTest(
    name='query_test',
    column_name='title',
    column_name_fallback=['title', 'pealkiri', '%song%'],
    expected_value='Madness of Love',
    where='test_id=1',
    points=20
)
```

#### Elements Checks

Use `elements` to require or ban SQL/source fragments. `should_exist=True` means the element is required; `should_exist=False` means it is banned.

```python
QueryStructureTest(
    name='query_test',
    elements='LIMIT',
    should_exist=False,
    title='Query must not use LIMIT',
    points=10
)
```

`elements` can be a string or list. Lists are checked item by item so feedback can identify the missing required elements or the banned elements that were found. `QueryStructureTest` checks the generated `query_view`, `ViewTest` checks view definitions, and `FunctionTest`/`ProcedureTest` check `pg_proc.prosrc`.

#### Debug Mode

Most tests and `ExecuteLayer` support `debug='DEBUG'` or `debug='ALL'`.

- `DEBUG` prints the test title, generated query, result, and feedback debugging information.
- `ALL` also prints the test object's configured fields, such as `name`, `column_name`, `expected_value`, `elements`, and `points`.
- SQL system errors print the exception and generated query when debug is enabled.

```python
StructureTest(
    name='users',
    column_name='email',
    debug='DEBUG',
    points=10
)
```

#### LLM Check

`llm_check=True` runs the generated query before the normal test execution and checks whether row existence matches `should_exist`. If the check fails, Silmused returns the `sys_fail.llm_check_fail` feedback message, or `custom_feedback` if one is provided.

```python
QueryStructureTest(
    name='query_test',
    elements='GROUP BY',
    should_exist=True,
    llm_check=True,
    custom_feedback='The query must use GROUP BY.',
    points=10
)
```

## Usage Patterns

### Database Testing Workflow

1. **Prepare Database:**
   ```bash
   pg_dump -U postgres mydatabase > mydb.sql
   ```

2. **Write Tests:**
   ```python
    from silmused.ChecksLayer import ChecksLayer
    from silmused import StructureTest, DataTest, ConstraintTest, TitleLayer
    
    tests = [
        TitleLayer('Homework 3'),
        ChecksLayer(
            title='Table Persons tests ',
            tests=[
                StructureTest(title='Does table Persons exists?',name='persons',points=30),
                DataTest(title='Does table Persons have correct rows of data?',name='persons',expected_value=17,points=20),
                ConstraintTest(title='Does the primary key exist?',name='persons',constraint_type='PRIMARY KEY',points=20),
                ConstraintTest(title='Does the unique constraint exist?',name='persons',constraint_type='UNIQUE',points=10),
            ]
        ),
        TitleLayer('Practical 3'),
        ChecksLayer(
            title='Table Clubs tests',
            tests=[
                StructureTest(title='Does column location exists?',name='clubs',column_name='location',points=30),
                DataTest(title='Is column location filled with data?',name='clubs',column_name='location',points=20),
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

The final `<encoding>` argument is optional. When omitted, `encoding=None` is passed to Python file reading. Query mode reads `<query_file>` as the submitted SQL query and uses `<query_test_database>` as the database dump or SQL script that provides the execution context. Invalid dump files, empty query files, and invalid `test_query` values are reported through translated `sys_fail` messages.

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
            StructureTest(name='users', column_name='created_at', expected_type='text', points=10),
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
  "producer": "silmused 1.7.8",
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
2. Test type, test key, and feedback parameters are determined
3. Translator looks up message in locale file
4. Parameters are substituted into message template
5. List parameters are rendered with localized separators, such as `or` in English and `või` in Estonian
6. Custom feedback (if provided) overrides default positive and negative feedback

Most tests use positional feedback parameters (`$param1`, `$param2`, etc.). Some newer feedback entries use named parameters, especially `IndexTest`, `TriggerTest`, and `ProcedureTest`.

### Result Structure

- **Root Level:**
  - `result_type`: Always `"OK_V3"`
  - `points`: Percentage score (0-100)
  - `producer`: Version string (e.g., `"silmused 1.7.8"`)
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

Some templates use named placeholders instead of positional placeholders:

```json
{
  "trigger_test": {
    "trigger_exists_negative_feedback": "Wrong, trigger '$trigger_name' was not found"
  }
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
- `custom_feedback` - Custom feedback wrapper

Newer feedback keys include required/banned `elements` messages for functions, procedures, views, materialized views, and query structure tests, plus expanded `sys_fail` messages for invalid dumps, empty query files, invalid test format, undefined database objects, ambiguous columns, round-function type errors, missing result indexes, and `llm_check` failures.

### Message Templates

Messages support parameter substitution using `$param1`, `$param2`, and so on. Named placeholders are also supported for messages that pass semantic parameter names.

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

Internally, custom feedback is routed through the `custom_feedback.custom_feedback` locale key, so custom messages participate in the same translation and formatting flow as default feedback.

## Development & Test Suite

Automated regression tests live in `automated-tests/`:

- `automated-tests/test_core/` - Unit tests for core classes such as `Runner`, `Translator`, `ChecksLayer`, `ExecuteLayer`, `TitleLayer`, and `TestDefinition`.
- `automated-tests/test_feedback/` - Feedback tests for every test type and system failure feedback.
- `automated-tests/integration/` - Integration-style tests using mocked PostgreSQL connections.

Run the test suite with pytest:

```bash
pytest automated-tests
```

Run focused subsets when developing feedback or integration behavior:

```bash
pytest automated-tests/test_feedback -v
pytest automated-tests/integration -v
```

Example test cases are no longer fully bundled as normal tracked files. The `silmused/test_cases` path is managed as a Git submodule backed by the private `silmused-test-cases` repository. After cloning, initialize submodules if you need those examples:

```bash
git submodule update --init
```

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
11. **Use `elements` sparingly** - It is best for checking required or banned SQL constructs, not for validating complete query correctness
12. **Use `debug='DEBUG'` while developing tests** - Remove or disable debug output before production grading runs
13. **Use `expected_value_query` for dynamic fixtures** - Prefer it when expected values depend on the imported database state

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

**Problem:** Query/view/function/procedure element checks give unexpected failures
- **Solution:** Remember that `should_exist=True` means required elements and `should_exist=False` means banned elements. Lists are checked item by item.

**Problem:** `column_name` lists fail in data tests
- **Solution:** `DataTest` and `QueryDataTest` expect a single string column name. Use `column_name_fallback` for acceptable alternatives.

**Problem:** Need to inspect generated SQL or raw results
- **Solution:** Add `debug='DEBUG'` or `debug='ALL'` to the test while developing.

**Problem:** LLM check fails with unfair-solution feedback
- **Solution:** Verify that `llm_check=True` is intentional and that the generated query returns rows when `should_exist=True`, or no rows when `should_exist=False`.

## Additional Resources

- Review `demo.py`, `query_demo.py`, and `demo_test_cases.py` for complete working examples
- Review `automated-tests/` for feedback, core, and integration regression tests

