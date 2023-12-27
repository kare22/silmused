import psycopg2 as psycopg2

from demo_test_cases import tests

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "karelpaan"
DB_PASSWORD = "postgresql"
DB_SCHEMA = "public"


def connect(db_name='postgres', auto_commit=False):
    connection_layer = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=db_name,
        user=DB_USER,
        password=DB_PASSWORD
    )

    if auto_commit:
        connection_layer.autocommit = True

    return connection_layer


connection = connect(db_name='koik', auto_commit=True)
cursor = connection.cursor()

results = []

for test in tests:
    results.append(test.run(cursor))

cursor.close()
connection.close()


for result in results:
    print(f"{result}")