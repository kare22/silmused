# from silmused.test_cases.query_tests.paring_koik import tests
#from silmused.test_cases.query_tests.euro_praks_6_2 import tests
from silmused.test_cases.query_tests.euro_kodu_6_4 import tests
from silmused.test_cases.query_tests.euro_querys import querys
from silmused.Runner import Runner

db_user = "postgres"
test_query = 'query'
lang = 'et'
#base_database_path = "silmused/test_cases/createdb.sql"
base_database_path = "silmused/test_cases/eurovisioon.sql"
query_sql_path = "silmused/test_cases/query.sql"
query_sql = ''
if test_query == 'query':
    file_path = base_database_path
    with open(query_sql_path, 'r') as file:
        query_sql = file.read()

for key in querys:
    r = Runner(file_path, tests, db_user=db_user, lang=lang, test_query=test_query, query_sql=querys[key], encoding="UTF-8")
    print(r.get_results())

#r = Runner(file_path, tests, db_user=db_user, lang=lang, test_query=test_query, query_sql=query_sql, encoding="UTF-8")
#print(r.get_results())
