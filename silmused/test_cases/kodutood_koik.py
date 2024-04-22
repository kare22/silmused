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

    # Kodutöö 5 kontrollid
    # 25p
    ChecksLayer(
        title='Funktsiooni f_vanus kontrollid',
        tests=[
            FunctionTest(
                title='Kas kuupäevaga 09.09.2000 on vanus õige?',
                name='f_vanus',
                arguments=['09.09.2000'],
                expected_value=23,
                points=12,
            ),
            FunctionTest(
                title='Kas kuupäevaga 01.01.2000 on vanus õige?',
                name='f_vanus',
                arguments=['01.01.2000'],
                expected_value=24,
                points=13,
            ),
        ]
    ),
    # 25p
    ChecksLayer(
        title='Funktsiooni f_klubiranking kontrollid',
        tests=[
            FunctionTest(
                title='Kas klubi Ajurebend ranking on õige?',
                name='f_klubiranking',
                arguments=[54],
                expected_value=1279.6,
                points=12,
            ),
            FunctionTest(
                title='Kas klubi Musta kivi kummardajad ranking on õige?',
                name='f_klubiranking',
                arguments=[59],
                expected_value=1407.0,
                points=13,
            ),
        ]
    ),
    # 25p
    ChecksLayer(
        title='Funktsiooni f_top10 kontrollid',
        tests=[
            FunctionTest(
                title='Kas on õige tulemuste arv?',
                name='f_top10',
                arguments=[44],
                expected_count=10,
                points=10,
            ),
            FunctionTest(
                title='Kas leidub mangija Murakas?',
                name='f_top10',
                where="mangija LIKE 'Murakas%'",
                arguments=[44],
                points=5,
            ),
            FunctionTest(
                title='Kas mangijal on õige paunktide arv?',
                name='f_top10',
                column_name='round(punkte,1)',
                where="mangija LIKE 'Muld%'",
                expected_value=5.5,
                arguments=[47],
                points=10,
            ),
        ]
    ),
tests = [
    # 25p
    ChecksLayer(
        title='Protseduuri sp_uus_turniir kontrollid',
        tests=[
            ProcedureTest(
                title='Kas on õige lõppkuupäev ühe päevasel turniiril?',
                name='sp_uus_turniir',
                arguments=['Tartu Meister', '02.02.2022',1,'Tartu'],
                number_of_parameters=4,
                pre_query="DELETE FROM turniirid WHERE nimi='Tartu Meister'",
                after_query="select * from turniirid where nimi = 'Tartu Meister' and loppkuupaev = '02.02.2022'",
                points=11,
            ),
            DataTest(
                title='Kas turniiriga lisati ka uus asula?',
                name='asulad',
                where="nimi = 'Haapsalu'",
                points=2,
            ),
            ProcedureTest(
                title='Kas on õige lõppkuupäev kahe päevasel turniiril?',
                name='sp_uus_turniir',
                arguments=['Tartu Meister', '02.02.2022',2,'Tartu'],
                number_of_parameters=4,
                pre_query="DELETE FROM turniirid WHERE nimi='Tartu Meister'",
                after_query="select * from turniirid where nimi = 'Tartu Meister' and loppkuupaev = '03.02.2022'",
                points=12,
            ),
            DataTest(
                title='uus turniir',
                name='turniirid',
                column_name='count(*)',
                where="nimi='Tartu Meister'",
                expected_value=0,
            ),
        ]
    ),
]
"""
_user1 = 123456
_user2 = 123457
_partii_id = 123123
tests = [
    # Kodutöö 6 kontrollid
    # 10p + 10p
    ChecksLayer(
        title='Indeksite kontrollid',
        tests=[
            IndexTest(
                title='Kas on olemas ix_riiginimi?',
                name='ix_riiginimi',
                points=10,
            ),
            IndexTest(
                title='Kas on olemas ix_suurus?',
                name='ix_suurus',
                points=10,
            ),
        ],
    ),
    # 25p
    ChecksLayer(
        title='Trigger tg_partiiaeg kontrollid',
        tests=[
            TriggerTest(
                title='Kas on õige definitsioon tg_partiiaeg?',
                name='tg_partiiaeg',
                arguments=['UPDATE', 'INSERT'],
                action_timing='BEFORE',
                points=10,
            ),
            ExecuteLayer("ALTER TABLE public.partiid DISABLE TRIGGER ALL"),
            ExecuteLayer("ALTER TABLE public.partiid ENABLE TRIGGER tg_partiiaeg"),
            ExecuteLayer("ALTER TABLE public.isikud DISABLE TRIGGER ALL"),
            ExecuteLayer(f"DELETE FROM public.isikud WHERE id in ({_user1},{_user2})"),
            ExecuteLayer(f"INSERT INTO public.isikud (id, eesnimi, perenimi) VALUES ({_user1},'Man', 'Ka')"),
            ExecuteLayer(f"INSERT INTO public.isikud (id, eesnimi, perenimi) VALUES ({_user2},'Kan', 'Ma')"),
            ExecuteLayer(f"INSERT INTO public.partiid VALUES (44,'2023-04-22 17:45:24.000','2023-03-22 17:45:24.000',{_user1},{_user2},2,0, {_partii_id})", ),
            DataTest(
                title='Kas testimiseks õnnestus lisada test_isik1?',
                name='isikud',
                where=f"public.isikud.id = {_user1} and EXISTS(SELECT * FROM information_schema.triggers WHERE trigger_name = 'tg_partiiaeg')",
                points=2,
            ),
            DataTest(
                title='Kas testimiseks õnnestus lisada test_isik2?',
                name='isikud',
                where=f"public.isikud.id = {_user2} and EXISTS(SELECT * FROM information_schema.triggers WHERE trigger_name = 'tg_partiiaeg')",
                points=2,
            ),
            DataTest(
                title='Kas testimiseks lisatud isikute partii lõpphetk on õige?',
                name='partiid',
                column_name='lopphetk',
                where=f"valge = {_user1} AND must = {_user2} and EXISTS(SELECT * FROM information_schema.triggers WHERE trigger_name = 'tg_partiiaeg')",
                expected_value='None',
                points=11,
            ),
        ],
    ),
    # 25p
    ChecksLayer(
        title='Trigger tg_klubi_olemasolu kontrollid',
        tests=[
            ExecuteLayer("ALTER TABLE public.partiid DISABLE TRIGGER ALL"),
            ExecuteLayer("ALTER TABLE public.isikud DISABLE TRIGGER ALL"),
            ExecuteLayer("ALTER TABLE public.isikud ENABLE TRIGGER tg_klubi_olemasolu"),
            ExecuteLayer(f"DELETE FROM public.isikud WHERE id in ({_user1},{_user2})"),
            ExecuteLayer(f"INSERT INTO public.isikud (id, eesnimi, perenimi) VALUES ({_user1},'Man', 'Ka')"),
            TriggerTest(
                title='Kas on õige definitsioon tg_klubi_olemasolu?',
                name='tg_klubi_olemasolu',
                arguments=['UPDATE', 'INSERT'],
                action_timing='AFTER',
                points=10,
            ),
            DataTest(
                title='Kas on olemas klubi Klubitud?',
                name='klubid',
                column_name='COUNT(*)',
                where="lower(nimi) = 'klubitud' and EXISTS(SELECT * FROM information_schema.triggers WHERE trigger_name = 'tg_klubi_olemasolu')",
                points=3,
            ),
            DataTest(
                title='Kas testimiseks õnnestus lisada test_isik1?',
                name='isikud',
                where=f"public.isikud.id = {_user1} and EXISTS(SELECT * FROM information_schema.triggers WHERE trigger_name = 'tg_klubi_olemasolu')",
                points=2,
            ),
            DataTest(
                title='Kas lisatud isik on klubis Klubitud?',
                name='isikud',
                join=f"public.klubid ON public.klubid.id=isikud.klubis",
                where=f"public.isikud.id = {_user1} AND public.klubid.nimi LIKE '%ubitu%' and EXISTS(SELECT * FROM information_schema.triggers WHERE trigger_name = 'tg_klubi_olemasolu')",
                points=10,
            ),
        ]
    )
]