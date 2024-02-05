# from test_cases.feedback_tests import tests
from test_cases.koik_praksid import tests
# from test_cases.demo_test_cases import tests
from silmused.Runner import Runner

db_user = "postgres"
# db_user = "karelpaan"
# file_path = "test_cases/kodutoo3.sql"
file_path = "test_cases/feedback_tests.sql"

r = Runner(file_path, tests, db_user=db_user, lang='en')

print(r.get_results())