import sys

from silmused.Runner import Runner

'''
CLI to integrate the solution with e.g. a Docker sultion.

NB! The tests file must include an array with the key "tests"!!
'''
if __name__ == "__main__":
    sql_file_path = sys.argv[1]
    tests_path = sys.argv[2]
    lang = sys.argv[3] if len(sys.argv) > 3 else 'en'

    with open(tests_path, 'r') as file:
        tests_file_content = file.read()

    exec(tests_file_content)

    Runner(sql_file_path, tests, lang)


# /Users/karelpaan/Projects/andmebaasid-auto-test/koik/test.backup
# /Users/karelpaan/Projects/silmused/demo_test_cases.py


