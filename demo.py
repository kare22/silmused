from demo_test_cases import tests
from silmused.Runner import Runner

db_user = "karelpaan"
file_path = "/Users/karelpaan/Projects/andmebaasid-auto-test/koik/test.backup"

r = Runner(file_path, tests, test_name='unoduo', db_user=db_user)

print(r.get_results())