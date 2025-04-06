# Silmused

# Current versions
* python @3.12
* psycopg2 @2.9.9

# Code reference
- [Code reference](#code-reference)
  * [Basics](#basics)
  * [Test Structure](#test-structure)
    + [TestDefinition](#testdefinition)
  * [Tests](#tests)
    + [ConstraintTest](#constrainttest)
    + [DataTest](#datatest)
    + [FunctionTest](#functiontest)
    + [IndexText](#indextext)
    + [ProcedureTest](#proceduretest)
    + [QueryDataTest](#querydatatest)
    + [QueryStructureTest](#querystructuretest)
    + [StructureTest](#structuretest)
    + [TriggerTest](#triggertest)
    + [ViewTest](#viewtest)
    + [ChecksLayer](#checkslayer)
    + [ExecuteLayer](#executelayer)
    + [TitleLayer](#titlelayer)
  * [Runner](#runner)
    + [Initialize](#initialize)
    + [Database creation](#database-creation)
    + [Results](#results)
    + [Feedback](#feedback)
  * [Translation](#translation)
  * [Custom feedback](#custom-feedback)
- [Running Demo Files](#running-demo-files)
  * [Database Test Demo](#database-test-demo)
  * [Query Test Demo](#query-test-demo)
## Basics
* private methods are noted with an underscore (`_`) at the start 

## Test Structure
### TestDefinition
This is the heart and soul of `Silmused` and defines how tests should behave.

:note: Some classes do not implicitly use this as they serve a different purpose:
* ExecuteLayer
* TitleLayer
* ChecksLayer

All arguments and their requirements that are used for all of the different tests:

| Argument Name                     | Type                          | Default  | Limits                                           | Description                                                                                                   |
|-----------------------------------|-------------------------------|----------|--------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| name                              | string                        | NOT None | cannot be empty, must be lowercased              | the name of table, view, function etc. that is testes                                                         |
| points                            | integer, float                | 0        |                                                  | the amount of points of given for a specific test                                                             |
| title                             | string                        | None     |                                                  | tests can be given a short description or what was tested                                                     |
| where                             | string                        | None     |                                                  | can be used to specify test queries                                                                           |
| join                              | string                        | None     | current limis is on join                         | can be used to add joins                                                                                      |
| column_name                       | string                        | None     | must be lowercased                               | the column that is checked for data mostly                                                                    |
| should_exist                      | boolean                       | True     |                                                  | if tested result should exist or not                                                                          |
| query                             | string                        | None     | shouldn't be used for tests, will be overwritten | test inner query used for testing results                                                                     |
| description                       | string                        | None     |                                                  | can be used to give tests more through description, not displayed anywhere                                    |
| arguments                         | list                          | None     |                                                  | used to give arguments for functions/procedures, can be used to check specific values from information_schema |
| expected_value                    | string, numerical, NULL, list | None     | None                                             | When the test should return an expected result can be a list to check a range or multiple results             |
| expected_character_maximum_length | integer                       | None     |                                                  | used to test table/view column maximum allowed size                                                           |
| expected_type                     | string                        | None     |                                                  | used to check table/view column type                                                                          |
| expected_count                    | integer                       | None     | only used for function and procedure tests       | used to check the outputted line count of functions or procedures                                             |
| pre_query                         | string                        | None     | used only in procedure tests                     | used to run queries that are necessary to run before procedures                                               |
| after_query                       | string                        | None     | used only in procedure tests                     | used to run queries after procedure test queries                                                              |
| custom_feedback                   | string                        | None     | will overwrite the test default feedback         | can be used to give custom feedback                                                                           |

## Tests
These are the classes used for writing tests. All of the test types use SQL queries from the database to check if the inputted file
is valid according to written test. For example database tables or views structure data is collected from postgresql
information_schema. For example view data is tested with sql queries where the tests expect the correct values for 
queries or correct amount of data. Each of the coming Tests will have examples how to use them and how it translates to
SQL query to show how it works.

There are 2 types of tests Query and Database tests.
So only QueryDataTest and QueryStructureTest is used to test queries, all other tests are used to test databases.


### ConstraintTest
Used for testing table or column constraints
Valid arguments:
* title
* name
* column_name
* constraint_name
* constraint_type
* description
* should_exist
* points
Simple example for table constraint
```
ConstraintTest(
    title='Does table X have unique constraint?',
    name='table_x',
    constraint_name='unique_table_x',
    constraint_type='UNIQUE',
    points=10,
    )
```

### DataTest
Used for testing database structures like tables or views data. Queries have a different [DataTest](#query-data-test).
### FunctionTest
Used for testing functions.
### IndexText
Used for testing indexes.
### ProcedureTest
Used for testing procedures.
### QueryDataTest
Used for testing query data. Querytests are special, because the inputted file is a query, then its used to
create a table named "query_test". For all query related tests use: name='query_test', where name means the table name.
Also The table has an extra column named "test_id", this column name can be used test if the order of the query is correct.
Valid arguments:
* title
* name
* column_name
* should_exist
* where
* join
* description
* expected_value
* custom_feedback
* points\

Some examples of Query tests: \

1. We want to check if the query returns correct amount of lines:\
title='A question for the test, which is displayed, when feedback is given'\
name='query_test' - Always the same for query tests.\
column_name='COUNT(*)' - We find the query result line count
expected_value=10 - the Query must have 10 lines for a normal result or count gives exactly 10.
points=20 - the amount fo points the test gives. Usually maximum is 100 as in the end all results are divided by 100 to give %.
```
  QueryDataTest(
      title='Kas on õige ridade arvuga tulemus?',
      name='query_test',
      column_name='COUNT(*)',
      expected_value=10,
      points=20,
  )
  select count(*) from query_test; 
  This should equal 10. if its 10, then the test gives 20p.
```
```
  QueryDataTest(
      title='Kas 1. kohal on õige laul?',
      name='query_test',
      column_name='pealkiri',
      where="test_id=1",
      expected_value="Madness of Love",
      points=30,
  )
  select pealkiri from query_test where test_id=1; 
  So test_id=1 means we check value in the first row of column pealkiri and the expected value is "Madness of Love"
```
```
  QueryDataTest(
      title='Kas on olemas riik Australia?',
      name='query_test',
      where="riik='Australia'",
      points=30,
  ),
  select * from query_test where riik = 'Australia';
  We don't always need to know the exact amount of lines a query returns, so this test just checks if the test query 
  returns more than 0, then its enough for the test.
```
```
  QueryDataTest(
      title='Kas ei ole olemas riiki Bulgaaria?',
      name='query_test',
      where="riik='Bulgaria'",
      should_exist=False,
      points=30,
  ),
  select * from query_test where riik = 'Bulgaria';
  Sometimes we need to check for values that shouldn't be displayed and then we use should_exist=False.
  As a default its always True.
```
As all test inputs are always between quotes, then sometimes " " and ' ' are used interchangeably.
For example where = "riik = 'Bulgaria'" Its due to SQL values in queries always have to be between ' ', 
then in tests the whole line has to be between " ".

In some special cases you need more than one set of " " or ' ' then this can be solved with python string concat rules.
For example:\
We have a query column called "Title beginning" and we check for value 'Dance'.
```
  QueryDataTest(
      title='Is there a title beginning "Dance"?',
      name='query_test',
      where='"Title beginning"' + "='Dance'",
      points=20,
  )
  
```
### QueryStructureTest
Used for testing query structure, mainly to test if query has needed columns.
Valid arguments:
* title
* name
* column_name
* arguments
* should_exist
* where
* description
* custom_feedback
* points
Some examples of Tests
```
  QueryStructureTest(
      title='Does column Title exists?',
      name='query_test',
      column_name='Title',
      points=20,
  )
```
```
  QueryStructureTest(
      title='Does column Name not exists?',
      name='query_test',
      column_name='Name',
      should_exist=False,
      points=20,
  )
```
### StructureTest
### TriggerTest
Used for testing triggers. 
These tests use ExecuteLayer commands to prepare for trigger testing. 
### ViewTest
Used for testing views.
### ChecksLayer
This is a Test Layer that can be used to hold together a group of tests and give an overall Title for that group.
ex.
```
ChecksLayer(
  title='Checks for table X'
  tests=[
    StructureTest(...),
    DataTest(...),
  ],
),
ChecksLayer(...)
```

### ExecuteLayer
Used to RUN extra querys between or before tests
### TitleLayer
Used to insert extra titles if needed.
## Runner
The bread and butter of Silmused. That does lots of stuff.
### Initialize
* backup_file_path - path to the file that creates the database that will be tested or where the queries will be executed on. 
* tests - list of tests 
* lang - language, which will be used for test feedbacks, default is english 
* test_name - if given, then it is used in database creation, so different test databases could be differentiated 
* db_user - user used for connecting to database, default is postgres 
* db_host - host used for connecting to database, default is localhost 
* db_password - password used fo connecting to database, default is postgresql 
* db_port - port used for connecting to database, default is 5432 
* test_query - parameter that decides if query tests or database tests are executed, default is database tests 
* query_sql - when test_query='test', then this query will be used to create view, where the tests will be executed on.
* encoding - can be used to specify in what encoding database files are
### Database creation
Creates a random named database based on random string and current datetime and connects to it.
For database creation it accepts pg_dump or SQL script.
### Results
### Feedback
Used to format all tests results in a json format. All test results go through Translator.
## Translation
Used to add different translations to Silmused. Translation files are located in silmused/locale. 
Translation files are in JSON format.
Translation is built upon Test Type ex. (IndexTest, ProcedureTest) and Test Key which is specified in Test files for different testing feedbacks
## Custom feedback
Every test has an argument **custom_feedback** that can be used to write your own custom feedback for all tests.
If some test feedbacks would make sense as a default feedback, then pull request add it yourself.
# Running Demo Files
## Database Test Demo
To run tests for database tests use demo.py
## Query Test Demo
To run tests for query tests use query_demo.py
## Running tests on command line
Silmused can be run as a command line program

silmused <database_dump_file> <tests_file> <db_user> <hostname> <port> <db_password> <test_language> <test_type> <query_test_database> encoding

### Database tests
silmused <database_dump_file> <tests_file> <db_user> <hostname> <port> <db_password> <test_language> test '' encoding

Example:
``silmused lahendus.sql tests.py postgres localhost 5433 postgres et``
### Query tests
silmused <query_file> <tests_file> <db_user> <hostname> <port> <db_password> <test_language> query <query_test_database> encoding

Example:
``silmused query.sql euro_kodu_3_2.py postgres localhost 5432 postgresql et query eurovisioon.sql UTF-8``