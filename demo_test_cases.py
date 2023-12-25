from ExecuteLayer import ExecuteLayer
from TitleLayer import TitleLayer
from tests.DataTest import DataTest
from tests.StructureTest import StructureTest
from tests.ConstraintTest import ConstraintTest
from tests.FunctionTest import FunctionTest
from tests.IndexTest import IndexTest
from tests.ProcedureTest import ProcedureTest
from tests.TriggerTest import TriggerTest
from tests.ViewTest import ViewTest

_user1 = 123456
_user2 = 123457
_partii_id = 123123

tests = [
    TitleLayer('Praktikum 3'),
    StructureTest(
        name='turniirid',
        column_name='asukoht',
        points=2,
    ),
    StructureTest(
        name='partiid',
        column_name='vastavus',
        points=1,
    ),
    ConstraintTest(
        name='isikud',
        constraint_name='un_isikukood',
        constraint_type='UNIQUE',
        points=0.5,
    ),
    ConstraintTest(
        name='isikud',
        constraint_name='nimi_unique',
        constraint_type='UNIQUE',
        should_exist=False,
        points=0.25,
    ),
    StructureTest(
        name='klubid',
        column_name='asukoht',
        arguments=['character_maximum_length'],
        expected_value=100,
        points=1,
    ),
    StructureTest(
        name='klubid',
        column_name='asukoht',
        points=1,
    ),

    TitleLayer('Praktikum 4'),
    StructureTest(
        name='asulad',
    ),
    DataTest(
        name='asulad',
    ),
    StructureTest(
        name='riigid',
    ),
    StructureTest(
        name='klubid',
        column_name='asula',
    ),
    DataTest(
        name='klubid',
        column_name='asula',
    ),
    ConstraintTest(
        name='klubid',
        constraint_type='PRIMARY KEY'
    ),
    StructureTest(
        name='klubid',
        column_name='askoht',
        should_exist=False,
    ),

    TitleLayer('Kodutöö 3'),
    DataTest(
        name='isikud',
        points=1,
    ),
    ConstraintTest(
        name='isikud',
        constraint_type='PRIMARY KEY',
    ),
    ConstraintTest(
        name='isikud',
        constraint_type='UNIQUE',
    ),
    ConstraintTest(
        name='isikud',
        constraint_type='CHECK',
    ),
    StructureTest(
        name='klubid',
        column_name='asula',
    ),
    DataTest(
        name='turniirid',
        column_name='asula'
    ),
    ConstraintTest(
        name='turniirid',
        constraint_type='FOREIGN KEY',
    ),
    StructureTest(
        name='klubid',
        column_name='asukoht',
        should_exist=False,
    ),
    StructureTest(
        name='klubid',
        column_name='toimumiskoht',
        should_exist=False,
    ),

    TitleLayer('Kodutöö 4'),
    TitleLayer('Vaade v_turniiripartiid'),
    StructureTest(
        name='v_turniiripartiid',
    ),
    StructureTest(
        name='v_turniiripartiid',
        column_name='turniir_nimi',
    ),
    StructureTest(
        name='v_turniiripartiid',
        column_name='toimumiskoht',
    ),
    StructureTest(
        name='v_turniiripartiid',
        column_name='partii_id',
    ),
    StructureTest(
        name='v_turniiripartiid',
        column_name='partii_algus',
    ),
    StructureTest(
        name='v_turniiripartiid',
        column_name='partii_lopp',
    ),
    StructureTest(
        name='v_turniiripartiid',
        column_name='kes_voitis',
    ),
    DataTest(
        name='v_turniiripartiid',
        column_name='COUNT(*)',
        expected_value=299,
    ),
    DataTest(
        name='v_turniiripartiid',
        column_name='LOWER(kes_voitis)',
        where='partii_id = 270',
        expected_value='valge',
    ),
    DataTest(
        name='v_turniiripartiid',
        column_name='LOWER(kes_voitis)',
        where='partii_id = 241',
        expected_value='must',
    ),
    DataTest(
        name='v_turniiripartiid',
        column_name='LOWER(kes_voitis)',
        where='partii_id = 193',
        expected_value='viik',
    ),
    TitleLayer('Vaade v_klubipartiikogused'),
    StructureTest(
        name='v_klubipartiikogused',
    ),
    StructureTest(
        name='v_klubipartiikogused',
        column_name='klubi_nimi',
    ),
    StructureTest(
        name='v_klubipartiikogused',
        column_name='partiisid',
    ),
    DataTest(
        name='v_klubipartiikogused',
        column_name='COUNT(*)',
        expected_value=12,
    ),
    DataTest(
        name='v_klubipartiikogused',
        column_name='SUM(partiisid)',
        expected_value=571,
    ),
    TitleLayer('Vaade v_keskminepartii'),
    StructureTest(
        name='v_keskminepartii',
    ),
    StructureTest(
        name='v_keskminepartii',
        column_name='turniiri_nimi',
    ),
    StructureTest(
        name='v_keskminepartii',
        column_name='keskmine_partii',
    ),
    DataTest(
        name='v_keskminepartii',
        column_name='COUNT(*)',
        expected_value=5,
    ),
    DataTest(
        name='v_keskminepartii',
        column_name='ROUND(keskmine_partii, 3)',
        where="turniiri_nimi = 'Plekkkarikas 2010'",
        expected_value=23.765,
    ),
    DataTest(
        name='v_keskminepartii',
        column_name='ROUND(keskmine_partii, 3)',
        where="turniiri_nimi = 'Kolme klubi kohtumine'",
        expected_value=23.040,
    ),
    TitleLayer('Materialseeritud vaade mv_vaate_kontroll'),
    DataTest(
        name='mv_partiide_arv_valgetega',
        column_name='COUNT(*)',
        expected_value=85,
    ),
    DataTest(
        name='mv_partiide_arv_valgetega',
        column_name='COUNT(*)',
        where="eesnimi = 'Tarmo' AND perenimi = 'Kooser'",
    ),
    DataTest(
        name='mv_partiide_arv_valgetega',
        column_name='MIN(partiisid_valgetega)',
        expected_value=0,
    ),
    DataTest(
        name='mv_partiide_arv_valgetega',
        column_name='MAX(partiisid_valgetega)',
        expected_value=14,
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
        number_of_columns=4,
        pre_query="DELETE FROM turniirid WHERE nimi='Tartu Meister'",
        after_query="select * from turniirid where nimi = 'Tartu Meister' and loppkuupaev = '02.02.2022'",
    ),
    ProcedureTest(
        name='sp_uus_turniir',
        arguments=['Tartu Meister', '02.02.2022',2,'Tartu'],
        number_of_columns=4,
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