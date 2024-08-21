from silmused import ViewTest
from silmused.ChecksLayer import ChecksLayer
from silmused.tests.DataTest import DataTest


"""
tests = [
    # Kodutöö 4 ülesanne 4
    ChecksLayer(
        title='Tabeli Isikud kontrollid',
        tests=[
            StructureTest(
                title='Kas tabeli nimi on muudetud nimeks Isikud?',
                name='isikud',
                points=25,
            ),
            StructureTest(
                title='Kas on loodud veerg elukoht?',
                name='isikud',
                column_name='elukoht',
                points=25,
            ),
            StructureTest(
                title='Kas on lisatud id numbriga veerg?',
                name='isikud',
                arguments=['COUNT(*)'],
                expected_value=9,
                points=25,
            ),
            DataTest(
                title='Kas tabelis isikud on andmed olemas?',
                name='isikud',
                points=25,
            ),
        ]
    ),
]"""
"""
tests = [
    # Praktikum 6 ül 1
    ChecksLayer(
        title='Vaate v_voidulaulud kontrollid',
        tests=[
            ViewTest(
                title='Kas on olemas vaade v_voidulaulud?',
                name='v_voidulaulud',
                points=10,
            ),
            ViewTest(
                title='Kas on olemas veerg kuupäev?',
                name='v_voidulaulud',
                column_name='kuupäev',
                points=10,
            ),
            ViewTest(
                title='Kas on olemas veerg riik?',
                name='v_voidulaulud',
                column_name='riik',
                points=10,
            ),
            ViewTest(
                title='Kas on olemas veerg laul?',
                name='v_voidulaulud',
                column_name='laul',
                points=10,
            ),
            DataTest(
                title='Kas on õige riik laulul TOY?',
                name='v_voidulaulud',
                column_name='riik',
                where="laul='TOY'",
                expected_value='Israel',
                isView=True,
                points=10,
            ),
            DataTest(
                title='Kas on õige finaali kuupäev laulul Heroes?',
                name='v_voidulaulud',
                column_name='kuupäev',
                where="laul='Heroes'",
                expected_value='2015-05-23',
                isView=True,
                points=10,
            )
        ]
    ),
]"""

tests = [
    ChecksLayer(
        title='Vaate v_ansamblid kontrollid',
        tests=[
            ViewTest(
                title='Kas om olemas vaade v_ansamblid?',
                name='v_ansamblid',
                points=10,
            ),
            ViewTest(
                title='Kas om olemas veerg linn?',
                name='v_ansamblid',
                column_name='linn',
                points=10,
            ),
            ViewTest(
                title='Kas om olemas veerg aasta?',
                name='v_ansamblid',
                column_name='aasta',
                points=10,
            ),
            ViewTest(
                title='Kas om olemas veerg pealkiri?',
                name='v_ansamblid',
                column_name='pealkiri',
                points=10,
            ),
            ViewTest(
                title='Kas om olemas veerg lavanimi?',
                name='v_ansamblid',
                column_name='lavanimi',
                points=10,
            ),
            DataTest(
                title='Kas on õige tulemuste arv?',
                name='v_ansamblid',
                column_name='COUNT(*)',
                expected_value=148,
                isView=True,
                points=25,
            ),
            DataTest(
                title='Kas on õige finaali kuupäev',
                name='v_ansamblid',
                column_name='aasta',
                where="lavanimi='Sinplus'",
                expected_value=2012,
                isView=True,
                points=25,
            )
        ]
    ),
    ChecksLayer(
        title='Vaate mv_samataht kontrollid',
        tests=[
            ViewTest(
                title='Kas om olemas vaade mv_samataht?',
                name='mv_samataht',
                isMaterialized=True,
                points=25,
            ),
            DataTest(
                title='Kas on õige tulemuste arv?',
                name='mv_samataht',
                column_name='COUNT(*)',
                expected_value=10,
                isView=True,
                points=25,
            ),
            DataTest(
                title='Kas on õige finaali kuupäev',
                name='mv_samataht',
                column_name='COUNT(*)',
                where="left(pealkiri,1)!=left(lavanimi,1)",
                expected_value=0,
                isView=True,
                points=50,
            )
        ]
    ),
    ChecksLayer(
        title='Vaate v_synniriigid kontrollid',
        tests=[
            ViewTest(
                title='Kas om olemas vaade v_synniriigid?',
                name='v_synniriigid',
                points=25,
            ),
            ViewTest(
                title='Kas om olemas veerg riik?',
                name='v_synniriigid',
                column_name='riik',
                points=10,
            ),
            ViewTest(
                title='Kas om olemas veerg lauljate arv?',
                name='v_synniriigid',
                column_name='lauljate arv',
                points=10,
            ),
            DataTest(
                title='Kas on õige tulemuste arv?',
                name='v_synniriigid',
                column_name='COUNT(*)',
                expected_value=64,
                isView=True,
                points=25,
            ),
            DataTest(
                title='Kas on õige suurim lauljate arv?',
                name='v_synniriigid',
                column_name='MAX("lauljate arv")',
                expected_value=17,
                isView=True,
                points=30,
            )
        ]
    ),
    ChecksLayer(
        title='Vaate v_kestus kontrollid',
        tests=[
            ViewTest(
                title='Kas om olemas vaade v_kestus?',
                name='v_kestus',
                points=20,
            ),
            ViewTest(
                title='Kas om olemas veerg kestus?',
                name='v_kestus',
                column_name='kestus',
                points=10,
            ),
            ViewTest(
                title='Kas om olemas veerg keskmised punktid?',
                name='v_kestus',
                column_name='keskmised punktid',
                points=10,
            ),
            ViewTest(
                title='Kas om olemas veerg koht finaalis?',
                name='v_kestus',
                column_name='koht finaalis',
                points=10,
            ),
            DataTest(
                title='Kas on õige tulemuste arv?',
                name='v_kestus',
                column_name='COUNT(*)',
                expected_value=59,
                isView=True,
                points=10,
            ),
            DataTest(
                title='Kas on õige kestus, kui keskmine koht on 1?',
                name='v_kestus',
                column_name='kestus',
                where='"koht finaalis"=1',
                expected_value='00:03:11',
                isView=True,
                points=20,
            ),
            DataTest(
                title='Kas on õigel kohal kõige kõrgemad keskmised punktid?',
                name='v_kestus',
                column_name='round("koht finaalis",0)',
                where='"keskmised punktid"=466',
                expected_value='2',
                isView=True,
                points=20,
            )
        ]
    ),
]