from tests import tests
from silmused.Runner import Runner

db_user = "postgres"
file_path = "test.sql"

r = Runner(file_path, tests, db_user=db_user)

print(r.get_results())