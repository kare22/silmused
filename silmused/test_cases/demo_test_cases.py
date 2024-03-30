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
ChecksLayer(
        title='',
        tests=[
            
        ]
    ),
"""
_user1 = 123456
_user2 = 123457
_partii_id = 123123

tests = [
    #TitleLayer('Praktikum 3'),
    ChecksLayer(
        title='Tabeli Turniirid kontrollid',
        tests=[
            StructureTest(
                title='Kas veerg asukoht on olemas?',
                name='turniirid',
                column_name='asukoht',
                should_exist=False,
                points=2,
                ),
            ]
        ),
    ChecksLayer(
        title='Tabeli Partiid kontrollid',
        tests=[
            StructureTest(
                title='Kas veerg vastavus on olemas?',
                name='partiid',
                column_name='vastavus',
                points=1,
                ),
            ]
        ),
    ChecksLayer(
        title='Tabeli Isikud kontrollid',
        tests=[
            ConstraintTest(
                title='Kas kitsendus un_isikukood on olemas?',
                name='isikud',
                constraint_name='un_isikukood',
                constraint_type='UNIQUE',
                points=0.5,
            ),
            ConstraintTest(
                title='Kas kitsendus un_isikukood on kustutatud?',
                name='isikud',
                constraint_name='nimi_unique',
                constraint_type='UNIQUE',
                should_exist=False,
                points=0.25,
            ),
            ]
        ),
    ChecksLayer(
        title='Tabeli Klubid kontrollid',
        tests=[
            StructureTest(
                title='Kas veerg asukoht on olemas?',
                name='klubid',
                column_name='asukoht',
                points=1,
            ),
            StructureTest(
                title='Kas veeru asukoha väärtuse maksimum suurus on õige?',
                name='klubid',
                column_name='asukoht',
                arguments=['character_maximum_length'],
                expected_value=100,
                points=1,
            ),
            ConstraintTest(
                title='Kas tabeli primaarvõti on olemas?',
                name='klubid',
                constraint_type='PRIMARY KEY',
                points=0.5,
            ),
        ]
    ),
    TitleLayer('Praktikum 4'),
    ChecksLayer(
        title='Tabeli Asulad kontrollid',
        tests=[
            StructureTest(
                title='Kas tabel Asulad on olemas?',
                name='asulad',
            ),
            DataTest(
                title='Kas tabelis on andmed olemas?',
                name='asulad',
            ),
        ]
    ),
    ChecksLayer(
        title='Tabeli Riigid kontrollid',
        tests=[
            StructureTest(
                title='Kas tabel Riigid on olemas?',
                name='riigid',
            ),
        ]
    ),
    ChecksLayer(
        title='Tabeli Klubid kontrollid',
        tests=[
            StructureTest(
                title='Kas veerg asula on olemas?',
                name='klubid',
                column_name='asula',
            ),
            DataTest(
                title='Kas veeru asula andmed on olemas?',
                name='klubid',
                column_name='asula',
            ),
            ConstraintTest(
                title='Kas tabeli primaarvõti on olemas?',
                name='klubid',
                constraint_type='PRIMARY KEY'
            ),
            StructureTest(
                title='Kas veerg asukoht on kustutatud?',
                name='klubid',
                column_name='asukoht',
                should_exist=False,
            ),
        ]
    ),
    TitleLayer('Kodutöö 3'),
    ChecksLayer(
        title='Tabeli Isikud kontrollid ',
        tests=[
            DataTest(
                title='Kas tabel Isikud on olemas?',
                name='isikud',
                points=1,
            ),
            ConstraintTest(
                title='Kas tabeli primaarvõti on olemas?',
                name='isikud',
                constraint_type='PRIMARY KEY',
                points=1,
            ),
            ConstraintTest(
                title='Kas tabelis on unikaalsuse kitsendus?',
                name='isikud',
                constraint_type='UNIQUE',
                points=1,
            ),
            ConstraintTest(
                title='Kas tabelis on check kitsendus?',
                name='isikud',
                constraint_type='CHECK',
                points=1,
            ),
        ]
    ),
    ChecksLayer(
        title='Tabeli Klubid kontrollid',
        tests=[
            StructureTest(
                title='Kas veerg asula on olemas?',
                name='klubid',
                column_name='asula',
                points=1,
            ),
            StructureTest(
                title='Kas veerg asukoht on kustutatud?',
                name='klubid',
                column_name='asukoht',
                should_exist=False,
                points=1,
            ),
            StructureTest(
                title='Kas veerg toimumiskoht on kustutatud?',
                name='klubid',
                column_name='toimumiskoht',
                should_exist=False,
                points=1,
            ),
        ]
    ),
    ChecksLayer(
        title='Tabeli Turniirid kontrollid',
        tests=[
           DataTest(
                title='Kas veerg asula on olemas?',
                name='turniirid',
                column_name='asula',
                points=1,
            ),
            ConstraintTest(
                title='Kas tabelis on välisvõti olemas?',
                name='turniirid',
                constraint_type='FOREIGN KEY',
                points=1,
            ), 
        ]
    ),
    TitleLayer('Kodutöö 4'),
    ChecksLayer(
        title='Vaate v_turniiripartiid kontrollid',
        tests=[
            StructureTest(
                title='Kas vaade v_turniiripartiid on olemas?',
                name='v_turniiripartiid',
                points=1,
            ),
            StructureTest(
                title='Kas veerg turniir_nimi on olemas?',
                name='v_turniiripartiid',
                column_name='turniir_nimi',
                points=1,
            ),
            StructureTest(
                title='Kas veerg toimumiskoht on olemas?',
                name='v_turniiripartiid',
                column_name='toimumiskoht',
                points=1,
            ),
            StructureTest(
                title='Kas veerg partii_id on olemas?',
                name='v_turniiripartiid',
                column_name='partii_id',
                points=1,
            ),
            StructureTest(
                title='Kas veerg partii_algus on olemas?',
                name='v_turniiripartiid',
                column_name='partii_algus',
                points=1,
            ),
            StructureTest(
                title='Kas veerg partii_lopp on olemas?',
                name='v_turniiripartiid',
                column_name='partii_lopp',
                points=1,
            ),
            StructureTest(
                title='Kas veerg kes_voitis on olemas?',
                name='v_turniiripartiid',
                column_name='kes_voitis',
            ),
            DataTest(
                title='Kas vaate andmete kogus on õige?',
                name='v_turniiripartiid',
                column_name='COUNT(*)',
                expected_value=299,
                points=1,
            ),
            DataTest(
                title='Kas partii 270 võitja tulemus on õige?',
                name='v_turniiripartiid',
                column_name='LOWER(kes_voitis)',
                where='partii_id = 270',
                expected_value='valge',
                points=1,
            ),
            DataTest(
                title='Kas partii 241 võitja tulemus on õige?',
                name='v_turniiripartiid',
                column_name='LOWER(kes_voitis)',
                where='partii_id = 241',
                expected_value='must',
                points=1,
            ),
            DataTest(
                title='Kas partii 193 sai viigi?',
                name='v_turniiripartiid',
                column_name='LOWER(kes_voitis)',
                where='partii_id = 193',
                expected_value='viik',
                points=1,
            ),
            
        ]
    ),
    ChecksLayer(
        title='Vaate v_klubipartiikogused kontrollid',
        tests=[
            StructureTest(
                title='Kas vaade v_klubipartiikogused on olemas?',
                name='v_klubipartiikogused',
                points=1,
            ),
            StructureTest(
                title='Kas veerg klubi_nimi on olemas?',
                name='v_klubipartiikogused',
                column_name='klubi_nimi',
                points=1,
            ),
            StructureTest(
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
                points=1,
            ),
            DataTest(
                title='Kas vaate partiide summa kokku on õige?',
                name='v_klubipartiikogused',
                column_name='SUM(partiisid)',
                expected_value=571,
                points=1,
            ), 
        ]
    ),
    
    ChecksLayer(
        title='Vaate v_keskminepartii kontrollid',
        tests=[
            StructureTest(
                title='Kas vaade v_keskminepartii on olemas?',
                name='v_keskminepartii',
                points=1,
            ),
            StructureTest(
                title='Kas veerg turniiri_nimi on olemas?',
                name='v_keskminepartii',
                column_name='turniiri_nimi',
                points=1,
            ),
            StructureTest(
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
                points=1,
            ),
            DataTest(
                title='Kas turniiril Plekkkarikas 2010 keskmine partii arv on õige?',
                name='v_keskminepartii',
                column_name='ROUND(keskmine_partii, 3)',
                where="turniiri_nimi = 'Plekkkarikas 2010'",
                expected_value=23.765,
                points=1,
            ),
            DataTest(
                title='Kas turniiril Kolme klubi kohtumine keskmine partii arv on õige?',
                name='v_keskminepartii',
                column_name='ROUND(keskmine_partii, 3)',
                where="turniiri_nimi = 'Kolme klubi kohtumine'",
                expected_value=23.040,
                points=1,
            ),
        ]
    ),
    ChecksLayer(
        title='Materialiseeritud vaate mv_partiide_arv_valgetega kontrollid',
        tests=[
            DataTest(
                title='Kas vaade mv_partiide_arv_valgetega on olemas?',
                name='mv_partiide_arv_valgetega',
                column_name='COUNT(*)',
                expected_value=85,
                points=1,
            ),
            DataTest(
                title='Kas leidub partii ühe mängijaga?',
                name='mv_partiide_arv_valgetega',
                column_name='COUNT(*)',
                where="eesnimi = 'Tarmo' AND perenimi = 'Kooser'",
                points=1,
            ),
            DataTest(
                title='Kas vaate kõige väikseim väärtus on õige?',
                name='mv_partiide_arv_valgetega',
                column_name='MIN(partiisid_valgetega)',
                expected_value=0,
                points=1,
            ),
            DataTest(
                title='Kas vaate kõige suurem väärtus on õige?',
                name='mv_partiide_arv_valgetega',
                column_name='MAX(partiisid_valgetega)',
                expected_value=14,
                points=1,
            )
        ]
    ),
    
    TitleLayer('Kodutöö 5'),
    TitleLayer('Funktsioon f_vanus'),
    FunctionTest(
        name='f_vanus',
        arguments=['09.09.2000'],
        expected_value=22,
    ),
    FunctionTest(
        name='f_vanus',
        arguments=['01.01.2000'],
        expected_value=23,
    ),
    TitleLayer('Funktsioon f_klubiranking'),
    FunctionTest(
        name='f_klubiranking',
        arguments=[54],
        expected_value=1279.6,
    ),
    FunctionTest(
        name='f_klubiranking',
        arguments=[59],
        expected_value=1407.0,
    ),
    TitleLayer('Funktsioon f_top10'),
    FunctionTest(
        name='f_top10',
        arguments=[44],
        expected_count=10,
    ),
    FunctionTest(
        name='f_top10',
        where="mangija LIKE 'Murakas%'",
        arguments=[44],
    ),
    TitleLayer('Protseduur sp_uus_turniir'),
    ProcedureTest(
        name='sp_uus_turniir',
        arguments=['Tartu Meister', '02.02.2022',1,'Tartu'],
        number_of_parameters=4,
        pre_query="DELETE FROM turniirid WHERE nimi='Tartu Meister'",
        after_query="select * from turniirid where nimi = 'Tartu Meister' and loppkuupaev = '02.02.2022'",
    ),
    ProcedureTest(
        name='sp_uus_turniir',
        arguments=['Tartu Meister', '02.02.2022',2,'Tartu'],
        number_of_parameters=4,
        pre_query="DELETE FROM turniirid WHERE nimi='Tartu Meister'",
        after_query="select * from turniirid where nimi = 'Tartu Meister' and loppkuupaev = '03.02.2022'",
    ),

    TitleLayer('Kodutöö 6'),
    IndexTest(
        name='ix_riiginimi',
    ),
    IndexTest(
        name='ix_suurus',
    ),
    TriggerTest(
        name='tg_partiiaeg',
        arguments=['UPDATE', 'INSERT'],
        action_timing='BEFORE',
    ),
    ExecuteLayer("ALTER TABLE public.partiid DISABLE TRIGGER ALL"),
    ExecuteLayer("ALTER TABLE public.partiid ENABLE TRIGGER tg_partiiaeg"),
    ExecuteLayer("ALTER TABLE public.isikud DISABLE TRIGGER ALL"),
    ExecuteLayer("ALTER TABLE public.isikud ENABLE TRIGGER tg_klubi_olemasolu"),
    ExecuteLayer(f"INSERT INTO public.isikud (id, eesnimi, perenimi) VALUES ({_user1},'Man', 'Ka')"),
    ExecuteLayer(f"INSERT INTO public.isikud (id, eesnimi, perenimi) VALUES ({_user2},'Kan', 'Ma')"),
    ExecuteLayer(f"INSERT INTO public.partiid VALUES (44,'2023-04-22 17:45:24.000','2023-03-22 17:45:24.000',{_user1},{_user2},2,0, {_partii_id})", ),
    DataTest(
        name='isikud',
        where=f"public.isikud.id = {_user1}",
    ),
    DataTest(
        name='isikud',
        where=f"public.isikud.id = {_user2}",
    ),
    DataTest(
        name='partiid',
        column_name='lopphetk',
        where=f"valge = {_user1} AND must = {_user2}",
        expected_value=None,
    ),
    TriggerTest(
        name='tg_klubi_olemasolu',
        arguments=['UPDATE', 'INSERT'],
        action_timing='AFTER',
    ),
    DataTest(
        name='isikud',
        join=f"public.klubid ON public.klubid.id=isikud.klubis",
        where=f"public.isikud.id = {_user1} AND public.klubid.nimi LIKE '%ubitu%'",
    ),

    TitleLayer('Praktikum 7'),

    TitleLayer('Praktikum 10'),
    FunctionTest(
        name='f_mangija_punktid_turniiril',
        arguments=['92,42'],
        expected_value=5.5,
    ),
    FunctionTest(
        name='f_infopump',
        expected_count=105,
    ),
    FunctionTest(
        name='f_klubisuurus',
        arguments=[54],
        expected_value=5,
    ),
    FunctionTest(
        name='f_nimi',
        arguments=['test', 'kesk'],
        expected_value='kesk, test',
    ),
    FunctionTest(
        name='f_mangija_koormus',
        arguments=[73],
        expected_value=18,
    ),
    FunctionTest(
        name='f_mangija_voite_turniiril',
        arguments=[197, 43],
        expected_value=3,
    ),
    FunctionTest(
        name='f_mangija_voite_turniiril',
        arguments=[75, 44],
        expected_value=0,
    ),
    FunctionTest(
        name='f_mangija_viike_turniiril',
        arguments=[197, 43],
        expected_value=1,
    ),
    FunctionTest(
        name='f_mangija_viike_turniiril',
        arguments=[75, 44],
        expected_value=0,
    ),
    FunctionTest(
        name='f_mangija_kaotusi_turniiril',
        arguments=[197, 43],
        expected_value=0,
    ),
    FunctionTest(
        name='f_mangija_kaotusi_turniiril',
        arguments=[75, 44],
        expected_value=2,
    ),
    FunctionTest(
        name='f_klubiparimad',
        arguments=['Areng'],
        expected_count=3,
    ),
    FunctionTest(
        name='f_klubiparimad',
        column_name='punktisumma',
        arguments=['Areng'],
        where="isik = 'Pőder, Priit'",
        expected_value=4.5,
    ),
    FunctionTest(
        name='f_voit_viik_kaotus',
        arguments=[44],
        expected_count=63,
    ),
    FunctionTest(
        name='f_voit_viik_kaotus',
        column_name='voite',
        where="id = 193",
        arguments=[44],
        expected_value=1,
    ),
    FunctionTest(
        name='f_voit_viik_kaotus',
        column_name='viike',
        where="id = 193",
        arguments=[44],
        expected_value=1,
    ),
    FunctionTest(
        name='f_voit_viik_kaotus',
        column_name='kaotusi',
        where="id = 193",
        arguments=[44],
        expected_value=0,
    ),
]