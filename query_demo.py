# from silmused.test_cases.query_tests.paring_koik import tests
#from silmused.test_cases.query_tests.eurovisioon_db.euro_praks_3_1 import tests
from silmused.test_cases.query_tests.eurovisioon.euro_kodu_2_1 import tests
from silmused.test_cases.query_tests.eurovisioon.euro_querys import querys
from silmused.Runner import Runner

db_user = "postgres"
test_query = 'query'
lang = 'et'
#base_database_path = "silmused/test_cases/ope_createdb.sql"
base_database_path = "silmused/test_cases/query_tests/eurovisioon/eurovisioon.sql"
query_sql_path = "silmused/test_cases/query_tests/eurovisioon/query.sql"

file_path = base_database_path
with open(query_sql_path, 'r') as file:
    query_sql = file.read()

for key in querys:
    # port 5432 is used by postgres v16
    # r = Runner(file_path, tests, db_user=db_user, db_port=5432, lang=lang, test_query=test_query,
    # query_sql=querys[key], encoding="UTF-8")

    # port 5433 is used by postgres v17
    r = Runner(file_path, tests, db_user=db_user, db_port=5433, lang=lang, test_query=test_query, query_sql=querys[key],
               encoding="UTF-8")
    print(r.get_results())

#r = Runner(file_path, tests, db_user=db_user, lang=lang, test_query=test_query, query_sql=query_sql, encoding="UTF-8")
#print(r.get_results())
