# from silmused.test_cases.feedback_tests import tests
#from silmused.test_cases.praksid_koik import tests
#from silmused.test_cases.kodutood_koik import tests
from silmused.test_cases.yldkontroll import tests
#from silmused.test_cases.single_test import tests
# from silmused.test_cases.demo_test_cases import tests
from silmused.Runner import Runner
import sys

db_user = "postgres"
lang = 'et'
# db_user = "karelpaan"
#file_path = "silmused/test_cases/praktikum12.sql"
file_path = "silmused/test_cases/kodutoo6.sql"
#file_path= "silmused/test_cases/tudeng.sql"
#file_path = "silmused/test_cases/feedback_tests.sql"


r = Runner(file_path, tests, db_user=db_user, lang=lang, encoding='')

print(r.get_results())