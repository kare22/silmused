# from feedback_tests import tests
from koik_praksid import tests
# from demo_test_cases import tests
from silmused.Runner import Runner

db_user = "postgres"
# db_user = "karelpaan"
#file_path = "kodutoo3.sql"
file_path = "feedback_tests.sql"

r = Runner(file_path, tests, db_user=db_user, lang='en')

print(r.get_results())