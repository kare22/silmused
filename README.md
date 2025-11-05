# Silmused

A PostgreSQL testing framework that validates database schemas and SQL queries automatically.

## What is Silmused?

Silmused helps you write automated tests for PostgreSQL databases. It can test:
- Database structures (tables, columns, constraints, indexes)
- Data content and correctness
- SQL query results and structure
- Functions and procedures
- Triggers and views

## Getting Started

### Prerequisites

- Python 3.12
- PostgreSQL database
- psycopg2 2.9.9

### Step 1: Prepare Your Database

Create a SQL dump file or SQL script with your database:

```bash
pg_dump -U postgres mydatabase > mydb.sql
```

Alternatively, you can use a SQL script file that contains INSERT statements.

### Step 2: Write Your First Test

Create a Python file (e.g., `my_tests.py`) with your tests:

```python
from silmused import Runner, StructureTest, DataTest

# Test that the 'users' table exists
test1 = StructureTest(
    name='users',
    title='Users table exists',
    points=10
)

# Test that users table has an email column
test2 = StructureTest(
    name='users',
    column_name='email',
    title='Email column exists',
    points=15
)

# Test that there are exactly 100 users
test3 = DataTest(
    name='users',
    column_name='COUNT(*)',
    expected_value=100,
    title='Correct number of users',
    points=20
)

tests = [test1, test2, test3]
```

### Step 3: Run Your Tests

```python
from silmused import Runner

runner = Runner(
    backup_file_path='mydb.sql',
    tests=tests,
    lang='en'
)

results = runner.get_results()
print(results)  # JSON output with test results
```

## Understanding Test Types

Silmused supports two main testing modes:

1. **Database Tests** - Test your database structure and data
2. **Query Tests** - Test SQL query results

### Database Tests

These tests validate your database schema and content.

#### Testing Table Structure

**Test if a table exists:**
```python
StructureTest(
    name='products',
    title='Products table exists',
    points=10
)
```

**Test if a column exists:**
```python
StructureTest(
    name='products',
    column_name='price',
    title='Price column exists',
    points=15
)
```

**Test column type:**
```python
StructureTest(
    name='products',
    column_name='price',
    expected_type='decimal',
    title='Price is decimal type',
    points=15
)
```

**Test column maximum length:**
```python
StructureTest(
    name='users',
    column_name='email',
    expected_type='varchar',
    expected_character_maximum_length=255,
    title='Email has correct length',
    points=10
)
```

#### Testing Data Content

**Check if data exists:**
```python
DataTest(
    name='orders',
    title='Orders table has data',
    points=10
)
```

**Check exact count:**
```python
DataTest(
    name='orders',
    column_name='COUNT(*)',
    expected_value=50,
    title='Exactly 50 orders',
    points=20
)
```

**Check specific value:**
```python
DataTest(
    name='users',
    column_name='email',
    where="id=1",
    expected_value='admin@example.com',
    title='First user has correct email',
    points=15
)
```

**Check value range:**
```python
DataTest(
    name='products',
    column_name='price',
    where="id=1",
    expected_value=[100, 200],  # Between 100 and 200
    title='Product price in range',
    points=20
)
```

**Check if value should NOT exist:**
```python
DataTest(
    name='users',
    where="deleted_at IS NOT NULL",
    should_exist=False,
    title='No deleted users',
    points=10
)
```

#### Testing Constraints

**Test table constraint:**
```python
ConstraintTest(
    name='users',
    title='Users table has constraints',
    points=10
)
```

**Test specific constraint type:**
```python
ConstraintTest(
    name='users',
    constraint_type='UNIQUE',
    column_name='email',
    title='Email has unique constraint',
    points=15
)
```

**Test constraint by name:**
```python
ConstraintTest(
    name='users',
    constraint_name='pk_users',
    constraint_type='PRIMARY KEY',
    title='Primary key constraint exists',
    points=20
)
```

#### Testing Functions

**Test function exists:**
```python
FunctionTest(
    name='calculate_total',
    arguments=[100, 0.2],
    title='Function returns value',
    points=20
)
```

**Test function return value:**
```python
FunctionTest(
    name='calculate_total',
    arguments=[100, 0.2],
    expected_value=120,
    title='Function calculates correctly',
    points=30
)
```

**Test function result count:**
```python
FunctionTest(
    name='get_active_users',
    expected_count=10,
    title='Function returns 10 users',
    points=25
)
```

**Test function parameter count:**
```python
FunctionTest(
    name='calculate_total',
    arguments=[100, 0.2],
    number_of_parameters=2,
    title='Function has 2 parameters',
    points=15
)
```

#### Testing Procedures

**Test procedure:**
```python
ProcedureTest(
    name='update_order_status',
    arguments=[1, 'completed'],
    after_query="SELECT * FROM orders WHERE id=1 AND status='completed'",
    expected_count=1,
    title='Procedure updates order',
    points=30
)
```

**With pre-query setup:**
```python
ProcedureTest(
    name='process_payment',
    arguments=[100, 'USD'],
    pre_query="INSERT INTO accounts (id, balance) VALUES (1, 1000)",
    after_query="SELECT balance FROM accounts WHERE id=1",
    title='Procedure processes payment',
    points=40
)
```

#### Testing Views

**Test view exists:**
```python
ViewTest(
    name='active_users',
    title='Active users view exists',
    points=15
)
```

**Test view column:**
```python
ViewTest(
    name='active_users',
    column_name='username',
    title='View has username column',
    points=10
)
```

**Test materialized view:**
```python
ViewTest(
    name='user_stats',
    isMaterialized=True,
    title='Materialized view exists',
    points=20
)
```

#### Testing Indexes

**Test index exists:**
```python
IndexTest(
    name='idx_user_email',
    title='Email index exists',
    points=15
)
```

#### Testing Triggers

**Test trigger exists:**
```python
TriggerTest(
    name='update_timestamp',
    title='Update timestamp trigger exists',
    points=20
)
```

**Test trigger with event manipulation:**
```python
TriggerTest(
    name='audit_log_trigger',
    arguments=['INSERT', 'UPDATE'],
    action_timing='AFTER',
    title='Trigger handles INSERT and UPDATE',
    points=30
)
```

### Query Tests

Query tests validate SQL query results. When testing queries, the input file is your SQL query, and it creates a temporary table called `query_test` with an extra `test_id` column for row ordering.

**Important:** For all query tests, always use `name='query_test'`.

#### Testing Query Structure

**Test if query has a column:**
```python
QueryStructureTest(
    name='query_test',
    column_name='Title',
    title='Query has Title column',
    points=20
)
```

**Test if query should NOT have a column:**
```python
QueryStructureTest(
    name='query_test',
    column_name='Name',
    should_exist=False,
    title='Query does not have Name column',
    points=15
)
```

#### Testing Query Data

**Check query result count:**
```python
QueryDataTest(
    name='query_test',
    column_name='COUNT(*)',
    expected_value=10,
    title='Query returns 10 rows',
    points=20
)
```

**Check first row value:**
```python
QueryDataTest(
    name='query_test',
    column_name='pealkiri',
    where="test_id=1",
    expected_value="Madness of Love",
    title='First row has correct value',
    points=30
)
```

**Check if value exists:**
```python
QueryDataTest(
    name='query_test',
    where="riik='Australia'",
    title='Query includes Australia',
    points=30
)
```

**Check if value should NOT exist:**
```python
QueryDataTest(
    name='query_test',
    where="riik='Bulgaria'",
    should_exist=False,
    title='Query does not include Bulgaria',
    points=30
)
```

**Check value range:**
```python
QueryDataTest(
    name='query_test',
    column_name='price',
    where="test_id=1",
    expected_value=[100, 200],
    title='Price is in range',
    points=25
)
```

## Organizing Tests with Layers

### ChecksLayer

Group related tests together:

```python
from silmused import ChecksLayer, StructureTest, DataTest, ConstraintTest

ChecksLayer(
    title='Users table validation',
    tests=[
        StructureTest(name='users', points=10),
        StructureTest(name='users', column_name='email', points=15),
        ConstraintTest(name='users', constraint_type='UNIQUE', column_name='email', points=20),
        DataTest(name='users', column_name='COUNT(*)', expected_value=100, points=25)
    ]
)
```

### TitleLayer

Add section titles to your test output:

```python
from silmused import TitleLayer

TitleLayer('Database Structure Tests')
# ... your tests here ...
TitleLayer('Data Validation Tests')
# ... more tests ...
```

### ExecuteLayer

Run SQL queries between tests (useful for trigger testing):

```python
from silmused import ExecuteLayer

ExecuteLayer("INSERT INTO users (email) VALUES ('test@example.com')")
# ... your trigger tests here ...
```

## Complete Workflow Examples

### Example 1: Testing a Complete Database

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
    ),
    TitleLayer('Products'),
    ChecksLayer(
        title='Products table',
        tests=[
            StructureTest(name='products', points=10),
            StructureTest(name='products', column_name='price', expected_type='decimal', points=15),
            DataTest(name='products', where="price > 100", points=20)
        ]
    )
]

runner = Runner(
    backup_file_path='database.sql',
    tests=tests,
    lang='en'
)

results = runner.get_results()
print(results)
```

### Example 2: Testing a SQL Query

```python
from silmused import Runner, QueryStructureTest, QueryDataTest

# Your query file contains the SQL query
# The query will be executed and results stored in query_test table

tests = [
    QueryStructureTest(
        name='query_test',
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
        where="test_id=1",
        expected_value="Madness of Love",
        title='First row is correct',
        points=30
    )
]

runner = Runner(
    backup_file_path='database.sql',  # Database for query execution
    tests=tests,
    test_query='query',  # Enable query test mode
    query_sql='SELECT * FROM songs ORDER BY id',  # Your SQL query
    lang='en'
)

results = runner.get_results()
print(results)
```

## Runner Configuration

The `Runner` class accepts these parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `backup_file_path` | string | **Required** | Path to SQL dump or SQL script file |
| `tests` | list | **Required** | List of test objects |
| `lang` | string | `'en'` | Language for feedback (`'en'` or `'et'`) |
| `test_name` | string | `''` | Optional name for test database |
| `db_user` | string | `'postgres'` | PostgreSQL username |
| `db_host` | string | `'localhost'` | Database host |
| `db_password` | string | `'postgres'` | Database password |
| `db_port` | string | `'5432'` | Database port |
| `test_query` | string | `'test'` | `'test'` for database tests, `'query'` for query tests |
| `query_sql` | string | `''` | SQL query string (for query tests) |
| `encoding` | string | `None` | File encoding (e.g., `'UTF-8'`) |

## Common Test Parameters

All test classes share common parameters from `TestDefinition`:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | string | **Required** | Table/view/function name (must be lowercase) |
| `points` | int/float | `0` | Points awarded for this test |
| `title` | string | `None` | Test description shown in feedback |
| `column_name` | string | `None` | Column name to test (must be lowercase) |
| `should_exist` | boolean | `True` | Whether result should exist |
| `expected_value` | any | `None` | Expected value, or list `[min, max]` for range |
| `where` | string | `None` | WHERE clause for filtering |
| `join` | string | `None` | JOIN clause (currently only INNER JOIN) |
| `description` | string | `None` | Internal description (not shown in feedback) |
| `custom_feedback` | string | `None` | Custom feedback message |

## String Handling in Queries

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

**For columns with spaces:**
```python
QueryDataTest(
    name='query_test',
    where='"Title beginning"' + "='Dance'",  # Column name with spaces
    points=20
)
```

## Understanding Results

Test results are returned as JSON in OK_V3 format:

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
    }
  ]
}
```

- `points`: Percentage score (0-100)
- `tests`: Array of test results
- `status`: `"PASS"` or `"FAIL"`
- `feedback`: Human-readable feedback message

## Running Tests from Command Line

Silmused can be run as a command-line program:

### Database Tests

```bash
silmused <database_dump_file> <tests_file> <db_user> <hostname> <port> <db_password> <test_language> test '' <encoding>
```

**Example:**
```bash
silmused lahendus.sql tests.py postgres localhost 5432 postgresql en test '' UTF-8
```

### Query Tests

```bash
silmused <query_file> <tests_file> <db_user> <hostname> <port> <db_password> <test_language> query <query_test_database> <encoding>
```

**Example:**
```bash
silmused query.sql euro_kodu_3_2.py postgres localhost 5432 postgresql en query eurovisioon.sql UTF-8
```

**Note:** The tests file must include an array with the key `"tests"`:

```python
tests = [
    StructureTest(...),
    DataTest(...)
]
```

## Translation Support

Silmused supports multiple languages for feedback messages. Currently supported:
- English (`'en'`)
- Estonian (`'et'`)

Set the language when creating the Runner:

```python
runner = Runner(
    backup_file_path='database.sql',
    tests=tests,
    lang='et'  # Estonian feedback
)
```

## Custom Feedback

Every test supports custom feedback messages:

```python
DataTest(
    name='users',
    column_name='COUNT(*)',
    expected_value=100,
    custom_feedback='Expected exactly 100 users, but found a different number',
    points=20
)
```

Custom feedback overwrites the default translated feedback messages.

## Tips and Best Practices

1. **Always use lowercase for table/column names** - Silmused expects lowercase names
2. **Use descriptive titles** - They appear in test results and help debugging
3. **Group related tests** - Use `ChecksLayer` to organize tests logically
4. **Set appropriate points** - Total points typically sum to 100 for percentage scoring
5. **Use `description` for internal notes** - Not shown in feedback, useful for documentation
6. **Test incrementally** - Start with structure tests, then data tests
7. **Handle edge cases** - Test both positive (`should_exist=True`) and negative (`should_exist=False`) cases

## Troubleshooting

**Problem:** Tests fail with "table not found"
- **Solution:** Ensure table names are lowercase in tests

**Problem:** Query tests not working
- **Solution:** Make sure `test_query='query'` and `query_sql` is set, and use `name='query_test'` for all query tests

**Problem:** Encoding errors
- **Solution:** Specify `encoding='UTF-8'` when loading SQL files with special characters

**Problem:** Database connection fails
- **Solution:** Check database credentials, host, port, and ensure PostgreSQL is running

## Current Versions

- Python: 3.12
- psycopg2: 2.9.9
- Silmused: 1.4.5

