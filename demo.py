from Runner import Runner
from demo_test_cases import tests

db_user = "karelpaan"
file_path = "/Users/karelpaan/Projects/andmebaasid-auto-test/koik/Mihkel-Rump.backup"

Runner(file_path, tests, test_name='unoduo', db_user=db_user)

