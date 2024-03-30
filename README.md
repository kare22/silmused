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
## Tests
These are the classes used for writing tests
### ConstraintTest
Used for testing table or column constraints

### DataTest
### FunctionTest
### IndexText
### ProcedureTest
### StructureTest
### TriggerTest
### ViewTest

### ChecksLayer
This is a Test Layer that can be used to hold together a group of tests and give an overall Title for that group.
ex.
```
ChecksLayer(
  title='Checks for table X'
  tests=[
    StructureTest(...),
  ],
),
ChecksLayer(...)
```

### ExecuteLayer
Used to RUN extra querys between or before tests
### TitleLayer

## Runner
