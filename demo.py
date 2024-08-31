# from silmused.test_cases.feedback_tests import tests
# #from silmused.test_cases.ope_db.praksid_koik import tests
# #from silmused.test_cases.ope_db.kodutood_koik import tests
# from silmused.test_cases.ope_db.yldkontroll import tests
# #from silmused.test_cases.single_test import tests
from silmused.test_cases.eurovisioon_db.eurovisioon import tests
# from silmused.test_cases.demo_test_cases import tests
from silmused.Runner import Runner

db_user = "postgres"
lang = 'et'
# db_user = "karelpaan"
file_path = "silmused/test_cases/ope_db/praktikum12.sql"
#file_path = "silmused/test_cases/ope_db/kodutoo6.sql"
#file_path = "silmused/test_cases/eurovisioon_db/eurovisioon_db.sql"
#file_path= "silmused/test_cases/tudeng.sql"
#file_path = "silmused/test_cases/feedback_tests.sql"


r = Runner(file_path, tests, db_user=db_user, lang=lang, encoding='UTF-8')

print(r.get_results())