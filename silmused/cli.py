import sys

from silmused.Runner import Runner

'''
CLI to integrate the solution with e.g. a Docker sultion.

NB! The tests file must include an array with the key "tests"!!
'''


def main():
    sql_file_path = sys.argv[1]
    tests_path = sys.argv[2]
    db_user = sys.argv[3] if len(sys.argv) > 3 else 'postgres'
    db_host = sys.argv[4] if len(sys.argv) > 4 else 'localhost'
    db_port = sys.argv[5] if len(sys.argv) > 5 else '5432'
    db_password = sys.argv[6] if len(sys.argv) > 6 else 'postgresql'
    lang = sys.argv[7] if len(sys.argv) > 7 else 'en'
    test_query = sys.argv[8] if len(sys.argv) > 8 else 'test'
    querydb_path = sys.argv[9] if len(sys.argv) > 9 else ''

    with open(tests_path, 'r') as file:
        tests_file_content = file.read()
    local_vars = {}
    exec(tests_file_content, globals(), local_vars)
    tests = local_vars.get('tests')

    query_sql = ''
    if test_query == 'query':
        with open(sql_file_path, 'r') as file:
            query_sql = file.read()
        # query_sql = sql_file_path
        sql_file_path = querydb_path

    r=Runner(sql_file_path, tests, db_user=db_user, db_host=db_host, db_port=db_port, db_password=db_password, lang=lang, test_query=test_query, query_sql=query_sql)
    print(r.get_results())