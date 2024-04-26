# from silmused.test_cases.feedback_tests import tests
from silmused.test_cases.praksid_koik import tests
#from silmused.test_cases.kodutood_koik import tests
from silmused.test_cases.paring_koik import tests
# from silmused.test_cases.demo_test_cases import tests
from silmused.Runner import Runner
import sys

db_user = "postgres"
# db_user = "karelpaan"
file_path = "silmused/test_cases/praktikum11.sql"
#file_path = "silmused/test_cases/kodutoo6.sql"
#file_path= "silmused/test_cases/tudeng.sql"
#file_path = "silmused/test_cases/feedback_tests.sql"
#test_query = 'test'
test_query = 'query'
querydb_path = "silmused/test_cases/createdb.sql"
query_sql_path="silmused/test_cases/query.sql"
query_sql=''
if test_query == 'query':
    file_path = querydb_path
    with open(query_sql_path, 'r') as file:
        query_sql = file.read()
    # query_sql = query_sql_path


r = Runner(file_path, tests, db_user=db_user, lang='en', test_query=test_query, query_sql=query_sql)

print(r.get_results())