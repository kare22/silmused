from silmused.ChecksLayer import ChecksLayer
from silmused.ExecuteLayer import ExecuteLayer
from silmused.tests.QueryStructureTest import QueryStructureTest
from silmused.tests.QueryDataTest import QueryDataTest
_user1 = 123456
_user2 = 123457
tests = [
    ChecksLayer(
        title='Ülesanne 3 Päringu kontrollid',
        tests=[
            QueryStructureTest(
                title='Kas on olemas veerg ränkingu klass?',
                name='query_test',
                column_name="ränkingu klass",
                points=10,
            ),
            QueryStructureTest(
                title='Kas on olemas veerg arv?',
                name='query_test',
                column_name='arv',
                points=10,
            ),
            QueryStructureTest(
                title='Kas lahenduses on kasutatud keelatud elemente?',
                name='query_test',
                elements='LIMIT',
                should_exist=False,
                points=10,
            ),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=4,
                points=10,
            ),
            QueryDataTest(
                title='Kas on õige arv mängijaid ränkinguga 1100?',
                name='query_test',
                column_name='arv',
                where='"ränkingu klass" = 1100',
                expected_value=25,
                points=10,
            ),
            QueryDataTest(
                title='Kas on õige ränking viimasel kohal?',
                name='query_test',
                column_name='"ränkingu klass"',
                where='test_id=4',
                expected_value=1300,
                points=10,
            ),
            ExecuteLayer(f"INSERT INTO public.isikud (id, eesnimi, perenimi, ranking) values ({_user1}, 'etest1', 'ptest1', 1600)"),
            ExecuteLayer(f"INSERT INTO public.isikud (id, eesnimi, perenimi, ranking) values ({_user2}, 'etest2', 'ptest2', 1600)"),
            ExecuteLayer("delete from isikud where id = 10;"),
            ExecuteLayer("delete from query_test"),
            ExecuteLayer("insert into query_test select * from query_view;"),
            QueryDataTest(
                title='Kas on õige ridade arvuga tulemus, kui on lisatud 2 uut isikut ränkiguga 1600?',
                name='query_test',
                column_name='COUNT(*)',
                expected_value=5,
                points=30,
            ),
            QueryDataTest(
                title='Kas on õige ränking esimesel kohal kui eemaldada üks isik 1100 ränkiguga?',
                name='query_test',
                column_name='"ränkingu klass"',
                where='test_id=5',
                expected_value=1100,
                points=10,
            ),
        ]
    ),
]