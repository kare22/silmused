from kodutoo3 import tests
from silmused.Runner import Runner

db_user = "postgres"
file_path = "test.sql"

r = Runner(file_path, tests, db_user=db_user, lang='et')

print(r.get_results())