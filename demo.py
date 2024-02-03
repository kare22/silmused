from feedback_tests import tests
from silmused.Runner import Runner

db_user = "postgres"
file_path = "kodutoo3.sql"

r = Runner(file_path, tests, db_user=db_user, lang='et')

print(r.get_results())