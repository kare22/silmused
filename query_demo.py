#from silmused.test_cases.paring_koik import tests
from silmused.test_cases.eurovisioon import tests
from silmused.Runner import Runner
import sys

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


r = Runner(file_path, tests, db_user=db_user, lang=lang, test_query=test_query, query_sql=query_sql, encoding="UTF-8")

print(r.get_results())