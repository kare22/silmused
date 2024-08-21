# Silmused

# Current versions
* python @3.10
* psycopg2 @2.9.9

# Code reference
## Basics
* private methods are noted with an underscore (`_`) at the start 

## Test Structure
### TestDefinition
This is the heart and soul of `Silmused` and defines how tests should behave.

:note: Some classes do not implicitly use this as they serve a different purpose.
* ExecuteLayer
* TitleLayer
* ChecksLayer

All arguments and their requirements that are used for all of the different tests:
* name - string | cannot be empty, must be lowercased | the name of table, view, function etc. that is testes
* points - integer, numeric | default is 0 | the amount of points of given for a specific test
* title - string | default is None | tests can be given a short description or what was tested
* where - string | default is None | can be used to specify test queries
* join - string | default is None, current limis is on join | can be used to add joins
* column_name - string | default is None, must be lowercased | the column that is checked for data mostly
* should_exist - True/False | default is True | if tested result should exist or not
* query - string | shouldn't be used for tests, will be overwritten | test inner query used for testing results
* description - string | default is None | can be used to give tests more through description, not displayed anywhere
* arguments=None
* expected_value=None
* expected_character_maximum_length=None
* expected_type=None
* expected_count=None
* pre_query=None
* after_query=None
## Tests
These are the classes used for writing tests
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
### FunctionTest
Used for testing functions.
### IndexText
Used for testing indexes.
### ProcedureTest
Used for testing procedures.
### QueryDataTest
Used for testing query data.
### QueryStructureTest
Used for testing query structure, mainly to test if query has needed columns.
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
