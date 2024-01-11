import sys

# from silmused.Runner import Runner

'''
CLI to integrate the solution with e.g. a Docker sultion.

NB! The tests file must include an array with the key "tests"!!
'''
def main():
    sql_file_path = sys.argv[1]
    tests_path = sys.argv[2]
    lang = sys.argv[3] if len(sys.argv) > 3 else 'en'
    db_user = sys.argv[4] if len(sys.argv) > 4 else None

    with open(tests_path, 'r') as file:
        tests_file_content = file.read()

    # exec(tests_file_content)

    # print(tests)
    # Runner(sql_file_path, tests, lang, db_user=db_user)