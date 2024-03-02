from silmused.TitleLayer import TitleLayer
from silmused.ChecksLayer import ChecksLayer
from silmused.ExecuteLayer import ExecuteLayer
from silmused.tests.DataTest import DataTest
from silmused.tests.StructureTest import StructureTest
from silmused.tests.ConstraintTest import ConstraintTest
from silmused.tests.FunctionTest import FunctionTest
from silmused.tests.IndexTest import IndexTest
from silmused.tests.ProcedureTest import ProcedureTest
from silmused.tests.TriggerTest import TriggerTest
from silmused.tests.ViewTest import ViewTest
"""
tests = [
    # Kodutöö 3

    # Ülesanne 1 (30p) ja 2 (10p)
    ChecksLayer(
        title='Tabeli Inimesed kontrollid',
        tests=[
            StructureTest(
                title='Kas tabel Inimesed on olemas?',
                name='inimesed',
                points=6,
            ),
            StructureTest(
                title='Kas veerg eesnimi on olemas?',
                name='inimesed',
                column_name='eesnimi',
                points=3,
            ),
            StructureTest(
                title='Kas veerg perenimi on olemas?',
                name='inimesed',
                column_name='perenimi',
                points=3,
            ),
            StructureTest(
                title='Kas veerg sugu on olemas?',
                name='inimesed',
                column_name='sugu',
                points=3,
            ),
            ConstraintTest(
                title='Kas veerul sugu on check kitsendus?',
                name='inimesed',
                #column_name='sugu',
                constraint_type='CHECK',
                points=3,
            ),
            StructureTest(
                title='Kas veerg synnipaev on olemas?',
                name='inimesed',
                column_name='synnipaev',
                points=3,
            ),
            StructureTest(
                title='Kas veerg sisestatud on olemas?',
                name='inimesed',
                column_name='sisestatud',
                points=3,
            ),
            StructureTest(
                title='Kas veerg isikukood on olemas?',
                name='inimesed',
                column_name='isikukood',
                points=3,
            ),
            ConstraintTest(
                title='Kas veerul isikukood on unikaalsuse kitsendus?',
                name='inimesed',
                column_name='isikukood',
                constraint_type='UNIQUE',
                points=3,
            ),
            DataTest(
                title='Kas tabelis inimesed on andmed olemas?',
            name='inimesed',
            points=10,
            ),
        ]
    ),
    # Ülesande 3 (10p), 4 (20p), 5 (20p), 6 (10p) kontroll
    ChecksLayer(
        title='Tabeli Turniirid kontrollid',
        tests=[
            # Ülesande 3
            StructureTest(
                title='Kas veerg asula on olemas?',
                name='turniirid',
                column_name='asula',
                points=10,
            ),
            # Ülesande 4
            DataTest(
                title='Kas veergu asula on väärtused sisestatud?',
                name='turniirid',
                column_name='asula',
                points=20,
            ),
            # Ülesande 5
            ConstraintTest(
                title='Kas tabelis on välisvõti olemas?',
                name='turniirid',
                constraint_type='FOREIGN KEY',
                points=20,
            ),
            # Ülesande 6 
            StructureTest(
                title='Kas veerg toimumiskoht on kustutatud?',
                name='turniirid',
                column_name=['toimumiskoht','asukoht'],
                should_exist=False,
                points=10,
            ),
        ]
    ),
]
"""
tests = [
    # Kodutöö 4 kontrollid
    ChecksLayer(
        title='Vaate v_turniiripartiid kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade v_turniiripartiid on olemas?',
                name='v_turniiripartiid',
                points=1,
            ),
            ViewTest(
                title='Kas veerg turniir_nimi on olemas?',
                name='v_turniiripartiid',
                column_name='turniir_nimi',
                points=1,
            ),
            ViewTest(
                title='Kas veerg toimumiskoht on olemas?',
                name='v_turniiripartiid',
                column_name='toimumiskoht',
                points=1,
            ),
            ViewTest(
                title='Kas veerg partii_id on olemas?',
                name='v_turniiripartiid',
                column_name='partii_id',
                points=1,
            ),
            ViewTest(
                title='Kas veerg partii_algus on olemas?',
                name='v_turniiripartiid',
                column_name='partii_algus',
                points=1,
            ),
            ViewTest(
                title='Kas veerg partii_lopp on olemas?',
                name='v_turniiripartiid',
                column_name='partii_lopp',
                points=1,
            ),
            ViewTest(
                title='Kas veerg kes_voitis on olemas?',
                name='v_turniiripartiid',
                column_name='kes_voitis',
            ),
            DataTest(
                title='Kas vaate andmete kogus on õige?',
                name='v_turniiripartiid',
                column_name='COUNT(*)',
                expected_value=299,
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas partii 270 võitja tulemus on õige?',
                name='v_turniiripartiid',
                column_name='LOWER(kes_voitis)',
                where='partii_id = 270',
                expected_value='valge',
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas partii 241 võitja tulemus on õige?',
                name='v_turniiripartiid',
                column_name='LOWER(kes_voitis)',
                where='partii_id = 241',
                expected_value='must',
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas partii 193 sai viigi?',
                name='v_turniiripartiid',
                column_name='LOWER(kes_voitis)',
                where='partii_id = 193',
                expected_value='viik',
                isView=True,
                points=1,
            ),

        ]
    ),
    ChecksLayer(
        title='Vaate v_klubipartiikogused kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade v_klubipartiikogused on olemas?',
                name='v_klubipartiikogused',
                points=1,
            ),
            ViewTest(
                title='Kas veerg klubi_nimi on olemas?',
                name='v_klubipartiikogused',
                column_name='klubi_nimi',
                points=1,
            ),
            ViewTest(
                title='Kas veerg partiisid on olemas?',
                name='v_klubipartiikogused',
                column_name='partiisid',
                points=1,
            ),
            DataTest(
                title='Kas vaate andmete kogus on õige?',
                name='v_klubipartiikogused',
                column_name='COUNT(*)',
                expected_value=12,
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas vaate partiide summa kokku on õige?',
                name='v_klubipartiikogused',
                column_name='SUM(partiisid)',
                expected_value=571,
                isView=True,
                points=1,
            ),
        ]
    ),

    ChecksLayer(
        title='Vaate v_keskminepartii kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade v_keskminepartii on olemas?',
                name='v_keskminepartii',
                points=1,
            ),
            ViewTest(
                title='Kas veerg turniiri_nimi on olemas?',
                name='v_keskminepartii',
                column_name='turniiri_nimi',
                points=1,
            ),
            ViewTest(
                title='Kas veerg keskmine_partii on olemas?',
                name='v_keskminepartii',
                column_name='keskmine_partii',
                points=1,
            ),
            DataTest(
                title='Kas vaate andmete kogus on õige?',
                name='v_keskminepartii',
                column_name='COUNT(*)',
                expected_value=5,
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas turniiril Plekkkarikas 2010 keskmine partii arv on õige?',
                name='v_keskminepartii',
                column_name='ROUND(keskmine_partii, 3)',
                where="turniiri_nimi = 'Plekkkarikas 2010'",
                expected_value=23.765,
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas turniiril Kolme klubi kohtumine keskmine partii arv on õige?',
                name='v_keskminepartii',
                column_name='ROUND(keskmine_partii, 3)',
                where="turniiri_nimi = 'Kolme klubi kohtumine'",
                expected_value=23.040,
                isView=True,
                points=1,
            ),
        ]
    ),
    ChecksLayer(
        title='Materialiseeritud vaate mv_partiide_arv_valgetega kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade mv_partiide_arv_valgetega on olemas?',
                name='mv_partiide_arv_valgetega',
                isMaterialized=True,
                points=1,
            ),
            DataTest(
                title='Kas vaate andmete kogus on õige?',
                name='mv_partiide_arv_valgetega',
                column_name='COUNT(*)',
                expected_value=85,
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas leidub partii ühe mängijaga?',
                name='mv_partiide_arv_valgetega',
                column_name='COUNT(*)',
                where="eesnimi = 'Tarmo' AND perenimi = 'Kooser'",
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas vaate kõige väikseim väärtus on õige?',
                name='mv_partiide_arv_valgetega',
                column_name='MIN(partiisid_valgetega)',
                expected_value=0,
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas vaate kõige suurem väärtus on õige?',
                name='mv_partiide_arv_valgetega',
                column_name='MAX(partiisid_valgetega)',
                expected_value=14,
                isView=True,
                points=1,
            )
        ]
    ),
]
