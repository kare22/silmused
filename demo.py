# from silmused.test_cases.feedback_tests import tests
#from silmused.test_cases.kodutood_koik import tests
from silmused.test_cases.praksid_koik import tests
# from silmused.test_cases.demo_test_cases import tests
from silmused.Runner import Runner

db_user = "postgres"
# db_user = "karelpaan"
file_path = "silmused/test_cases/praktikum8.sql"
#file_path = "silmused/test_cases/feedback_tests.sql"

r = Runner(file_path, tests, db_user=db_user, lang='et')

print(r.get_results())