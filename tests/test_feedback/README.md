# Feedback Type Tests

This directory contains comprehensive tests for all feedback types in the Silmused framework. These tests verify that feedback messages are correctly generated, translated, and formatted for both success and failure scenarios.

## Test Coverage

### Test Files

1. **test_datatest_feedback.py** - Tests for DataTest feedback messages
   - Table and view data feedback
   - Expected value feedback (single, grouped numbers, grouped strings)
   - Should exist/should not exist scenarios

2. **test_structuretest_feedback.py** - Tests for StructureTest feedback messages
   - Table and column existence feedback
   - Type checking feedback
   - Character maximum length feedback

3. **test_constrainttest_feedback.py** - Tests for ConstraintTest feedback messages
   - Table and column constraint feedback
   - Constraint name and type combinations
   - Multi-column constraint feedback

4. **test_querydatatest_feedback.py** - Tests for QueryDataTest feedback messages
   - Query result feedback
   - Expected value feedback for queries
   - Grouped value feedback

5. **test_querystructuretest_feedback.py** - Tests for QueryStructureTest feedback messages
   - Query table and column structure feedback

6. **test_functiontest_feedback.py** - Tests for FunctionTest feedback messages
   - Function existence and type feedback
   - Parameter count feedback
   - Function result feedback

7. **test_proceduretest_feedback.py** - Tests for ProcedureTest feedback messages
   - Procedure existence and type feedback
   - Parameter count feedback
   - Procedure result count feedback

8. **test_viewtest_feedback.py** - Tests for ViewTest feedback messages
   - View and column existence feedback
   - Materialized view feedback

9. **test_indextest_feedback.py** - Tests for IndexTest feedback messages
   - Index existence feedback

10. **test_triggertest_feedback.py** - Tests for TriggerTest feedback messages
    - Trigger existence feedback
    - Trigger definition feedback

11. **test_sys_fail_feedback.py** - Tests for system failure feedback messages
    - Undefined column/table errors
    - Ambiguous column errors
    - Function errors
    - Index errors
    - Generic exception handling

## Running Tests

```bash
# Run all feedback tests
pytest tests/test_feedback/ -v

# Run specific test file
pytest tests/test_feedback/test_datatest_feedback.py -v

# Run with markers
pytest tests/test_feedback/ -m feedback -v
```

## Test Structure

Each test file follows a consistent structure:
- Tests are organized by feedback key
- Both positive and negative feedback scenarios are tested
- Mock database cursors are used to control test outcomes
- Tests verify feedback message structure and content

## Fixtures

Shared fixtures are available in `conftest.py`:
- `mock_cursor` - Mock database cursor
- `mock_connection` - Mock database connection
- Sample result fixtures for different query types

## Success Criteria

All tests verify:
- Correct feedback message structure
- Correct test_type and test_key
- Parameter substitution works correctly
- Custom feedback overrides default messages
- System failures generate appropriate error messages

