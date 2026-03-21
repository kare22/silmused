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

_user1 = 123456
_user2 = 123457
_partii_id = 123123
_asula_id = 200
_asula_nimi = 'Test_asula'
_klubi_id = 201
_klubi_nimi = 'Klubi kustutamiseks'

tests = [
    # Prakikum 3
    # Ülesanne 1, 14; 10p
    ChecksLayer(
        title='Prakikum 3 Tabeli Turniirid kontrollid',
        tests=[
            # 1
            StructureTest(
                title='Kas veerg toimumiskoht on kustutatud?',
                name='turniirid',
                column_name='toimumiskoht',
                should_exist=False,
                points=2,
            ),
            # 1
            # StructureTest(
            #    title='Kas veerg asukoht on olemas?',
            #    name='turniirid',
            #    column_name='asukoht',
            #    points=3,
            #    ),
            # 14
            ConstraintTest(
                title='Kas kitsendus ajakontroll on olemas?',
                name='turniirid',
                constraint_name='ajakontroll',
                points=5,
            ),
        ]
    ),
    # Ülesanne 2, 3, 4, 5 ja 8, 9, 12, 17, 18; 9 ül = 35p
    ChecksLayer(
        title='Prakikum 3 Tabeli Isikud kontrollid',
        tests=[
            # 2 ja 4
            StructureTest(
                title='Kas veerg Sisestatud on kustutatud?',
                name='isikud',
                column_name='sisestatud',
                should_exist=False,
                points=3,
            ),
            # 3
            ConstraintTest(
                title='Kas kitsendus un_isikukood on olemas?',
                name='isikud',
                column_name='isikukood',
                constraint_name='un_isikukood',
                constraint_type='UNIQUE',
                points=4,
            ),
            # 5
            ConstraintTest(
                title='Kas kitsendus isikud_un1 on kustutatud?',
                name='isikud',
                constraint_name='isikud_un1',
                constraint_type='UNIQUE',
                should_exist=False,
                points=2,
            ),
            # 8
            DataTest(
                title='Kas isiku Irys perenimi on muudetud?',
                name='isikud',
                column_name='perenimi',
                where="eesnimi = 'Irys'",
                expected_value='Kompvek',
                points=3,
            ),
            # 10
            DataTest(
                title='Kas P-tähega isikud on kustutatud?',
                name='isikud',
                column_name='COUNT(*)',
                where="eesnimi LIKE 'P%' AND RIGHT(eesnimi,1)='P'",
                expected_value=0,
                points=1,
            ),
            # 12
            StructureTest(
                title='Kas veerg klubis on olemas?',
                name='isikud',
                column_name='klubis',
                points=10,
            ),
            # 17
            DataTest(
                title='Kas Siim Susi on klubis Laudnikud?',
                name='isikud',
                column_name='COUNT(*)',
                where="eesnimi = 'Siim' AND perenimi = 'Susi' AND klubis = (select id from klubid where nimi = 'Laudnikud')",
                expected_value=1,
                points=5,
            ),
            # 18
            DataTest(
                title='Kas on lisatud 5 liiget klubisse Osav Oda?',
                name='isikud',
                column_name='COUNT(*)',
                where="klubis = (select id from klubid where nimi ilike 'osav oda')",
                expected_value=5,
                points=7,
            ),
        ]
    ),
    # 9; 15p
    ChecksLayer(
        title='Prakikum 3 Õ tähtede vahetamise kontrollid',
        tests=[
            DataTest(
                title='Kas isikute tabelis veerus eesnimi on "õ" tähed vahetatud?',
                name='isikud',
                column_name='eesnimi',
                where="eesnimi LIKE '%õ%'",
                points=5,
            ),
            DataTest(
                title='Kas isikute tabelis veerus perenimi on "õ" tähed vahetatud?',
                name='isikud',
                column_name='perenimi',
                where="perenimi LIKE '%õ%'",
                points=5,
            ),
            DataTest(
                title='Kas turniiride tabelis veerus nimi on "õ" tähed vahetatud?',
                name='turniirid',
                column_name='nimi',
                where="nimi LIKE '%õ%'",
                points=5,
            ),
        ],
    ),
    # Ülesanne 6, 13, 15; 20p
    ChecksLayer(
        title='Prakikum 3 Tabeli Partiid kontrollid',
        tests=[
            # 6
            ConstraintTest(
                title='Kas kitsendus vastavus on olemas?',
                name='partiid',
                constraint_name='vastavus',
                constraint_type='CHECK',
                points=5,
            ),
            # 13
            StructureTest(
                title='Kas veerg Kokkuvote on kustutatud?',
                name='partiid',
                column_name='kokkuvote',
                should_exist=False,
                points=5,
            ),
            # 15
            ConstraintTest(
                title='Kas kitsendus ajakontroll on olemas?',
                name='partiid',
                constraint_name='ajakontroll',
                points=10,
            ),
        ]
    ),
    # Ülesanne 7, 11, 16; 20p
    ChecksLayer(
        title='Prakikum 3 Tabeli Klubid kontrollid',
        tests=[
            # 7
            # StructureTest(
            #    title='Kas veeru asukoha väärtuse maksimum suurus on õige?',
            #    name='klubid',
            #    column_name='asukoht',
            #    expected_character_maximum_length=100,
            #    points=5,
            # ),
            # 11
            DataTest(
                title='Kas klubi osav oda on olemas?',
                name='klubid',
                where="nimi ilike 'Osav oda'",
                points=10,
            ),
            # 16
            # DataTest(
            #    title='Kas klubi Valge mask asukoht on Valga?',
            #    name='klubid',
            #    column_name='asukoht',
            #    where="nimi = 'Valge Mask'",
            #    expected_value='Valga',
            #    points=5,
            # ),
            # 16, aga üldtesti jaoks pärast praktikum 4
            DataTest(
                title='Kas klubi Valge mask asukoht on Valga?',
                name='klubid',
                column_name='nimi',
                where="nimi = 'Valge Mask' and asula = (select id from asulad where nimi = 'Valga')",
                expected_value='Valge Mask',
                points=5,
            ),
        ]
    ),

    # Praktikum 4
    # Ülesanne 1, 4, 40p
    ChecksLayer(
        title='Prakikum 4 Tabeli Asulad kontrollid',
        tests=[
            StructureTest(
                title='Kas tabel asulad on olemas?',
                name='asulad',
                points=15,
            ),
            StructureTest(
                title='Kas veerg id on olemas?',
                name='asulad',
                column_name='id',
                points=3,
            ),
            StructureTest(
                title='Kas veerg nimi on olemas?',
                name='asulad',
                column_name='nimi',
                points=3,
            ),
            ConstraintTest(
                title='Kas tabeli primaarvõti on olemas?',
                name='asulad',
                constraint_type='PRIMARY KEY',
                points=2,
            ),
            ConstraintTest(
                title='Kas tabelis on unikaalsuse kitsendus?',
                name='asulad',
                constraint_type='UNIQUE',
                points=2,
            ),
            # 4
            DataTest(
                title='Kas tabelis asulad on andmed olemas?',
                name='asulad',
                points=15,
            ),
        ]
    ),
    # Ülesanne 2, 3, 20p
    ChecksLayer(
        title='Prakikum 4 Tabeli Riigid kontrollid',
        tests=[
            StructureTest(
                title='Kas tabel riigid on olemas?',
                name='riigid',
                points=5,
            ),
            StructureTest(
                title='Kas veerg id on olemas?',
                name='riigid',
                column_name='id',
                points=1,
            ),
            StructureTest(
                title='Kas veerg nimi on olemas?',
                name='riigid',
                column_name='nimi',
                points=1,
            ),
            StructureTest(
                title='Kas veerg pealinn on olemas?',
                name='riigid',
                column_name='pealinn',
                points=1,
            ),
            StructureTest(
                title='Kas veerg rahvaarv on olemas?',
                name='riigid',
                column_name='rahvaarv',
                points=1,
            ),
            StructureTest(
                title='Kas veerg pindala on olemas?',
                name='riigid',
                column_name='pindala',
                points=1,
            ),
            StructureTest(
                title='Kas veerg skp_mld on olemas?',
                name='riigid',
                column_name='skp_mld',
                points=1,
            ),
            ConstraintTest(
                title='Kas tabeli primaarvõti on olemas?',
                name='asulad',
                constraint_type='PRIMARY KEY',
                points=2,
            ),
            ConstraintTest(
                title='Kas tabelis on unikaalsuse kitsendus?',
                name='asulad',
                constraint_type='UNIQUE',
                points=2,
            ),
            DataTest(
                title='Kas tabelis riigid on andmed olemas?',
                name='riigid',
                points=5,
            ),
        ]
    ),
    # Ülesanne 5, 6, 7, 9, 40p
    ChecksLayer(
        title='Prakikum 4 Tabeli Klubid kontrollid',
        tests=[
            StructureTest(
                title='Kas veerg asula on olemas?',
                name='klubid',
                column_name='asula',
                points=10,
            ),
            DataTest(
                title='Kas veerus asula on andmed olemas?',
                name='klubid',
                column_name='asula',
                points=10,
            ),
            StructureTest(
                title='Kas veerg asukoht on kustutatud?',
                name='klubid',
                column_name='asukoht',
                should_exist=False,
                points=5,
            ),
            StructureTest(
                title='Kas veerg toimumiskoht on kustutatud?',
                name='klubid',
                column_name='toimumiskoht',
                should_exist=False,
                points=5,
            ),
            ConstraintTest(
                title='Kas tabelis on välisvõti olemas?',
                name='klubid',
                constraint_type='FOREIGN KEY',
                points=10,
            ),

        ]
    ),

    # Kodutöö 3
    # Ülesanne 1 ja 2
    ChecksLayer(
        title='Kodutöö 3 Tabeli Inimesed kontrollid',
        tests=[
            StructureTest(
                title='Kas tabel Inimesed on olemas?',
                name='inimesed',
                points=1,
            ),
            StructureTest(
                title='Kas veerg eesnimi on olemas?',
                name='inimesed',
                column_name='eesnimi',
                points=1,
            ),
            StructureTest(
                title='Kas veerg perenimi on olemas?',
                name='inimesed',
                column_name='perenimi',
                points=1,
            ),
            StructureTest(
                title='Kas veerg sugu on olemas?',
                name='inimesed',
                column_name='sugu',
                points=1,
            ),
            ConstraintTest(
                title='Kas veerul sugu on check kitsendus?',
                name='inimesed',
                column_name='sugu',
                constraint_type='CHECK',
                points=1,
            ),
            StructureTest(
                title='Kas veerg synnipaev on olemas?',
                name='inimesed',
                column_name='synnipaev',
                points=1,
            ),
            StructureTest(
                title='Kas veerg sisestatud on olemas?',
                name='inimesed',
                column_name='sisestatud',
                points=1,
            ),
            StructureTest(
                title='Kas veerg isikukood on olemas?',
                name='inimesed',
                column_name='isikukood',
                points=1,
            ),
            ConstraintTest(
                title='Kas veerul isikukood on unikaalsuse kitsendus?',
                name='inimesed',
                column_name='isikukood',
                constraint_type='UNIQUE',
                points=1,
            ),
            DataTest(
                title='Kas tabelis inimesed on andmed olemas?',
                name='inimesed',
                points=1,
            ),
        ]
    ),
    # Ülesande 3, 4, 5, 6 kontroll
    ChecksLayer(
        title='Kodutöö 3 Tabeli Turniirid kontrollid',
        tests=[
            # Ülesande 3
            StructureTest(
                title='Kas veerg asula on olemas?',
                name='turniirid',
                column_name='asula',
                points=1,
            ),
            # Ülesande 4
            DataTest(
                title='Kas veergu asula on väärtused sisestatud?',
                name='turniirid',
                column_name='asula',
                points=1,
            ),
            # Ülesande 5
            ConstraintTest(
                title='Kas tabelis on välisvõti olemas?',
                name='turniirid',
                constraint_type='FOREIGN KEY',
                points=1,
            ),
            # Ülesande 6 kontrollid
            StructureTest(
                title='Kas veerg toimumiskoht on kustutatud?',
                name='turniirid',
                column_name='toimumiskoht',
                should_exist=False,
                points=0.5,
            ),
            StructureTest(
                title='Kas veerg asukoht on kustutatud?',
                name='turniirid',
                column_name='asukoht',
                should_exist=False,
                points=0.5,
            ),
        ]
    ),
    # Kodutöö 4 kontrollid
    ChecksLayer(
        title='Kodutöö 4 vaate v_turniiripartiid kontrollid',
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
            DataTest(
                title='Kas veerg toimumiskoht sisaldab andmeid?',
                name='v_turniiripartiid',
                column_name='COUNT(*)',
                where='toimumiskoht IS NOT NULL',
                isView=True,
                points=1,
            ),
        ]
    ),
    ChecksLayer(
        title='Kodutöö 4 vaate v_klubipartiikogused kontrollid',
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
        title='Kodutöö 4 vaate v_keskminepartii kontrollid',
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
                column_name='ROUND(keskmine_partii, 2)',
                where="turniiri_nimi = 'Kolme klubi kohtumine'",
                expected_value=23.04,
                isView=True,
                points=1,
            ),
        ]
    ),
    ChecksLayer(
        title='Kodutöö 4 materialiseeritud vaate mv_partiide_arv_valgetega kontrollid',
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
    # Praktikum 9 100p
    # 1; 2p
    ChecksLayer(
        title='Praktikum 9 vaate v_isikudklubid kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade v_isikudklubid on olemas?',
                name='v_isikudklubid',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='v_isikudklubid',
                isView=True,
                points=1,
            )
        ],
    ),
    # 2; 2p
    ChecksLayer(
        title='Praktikum 9 vaate v_partiid kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade v_partiid on olemas?',
                name='v_partiid',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='v_partiid',
                isView=True,
                points=1,
            )
        ],
    ),
    # 5; 11p
    ChecksLayer(
        title='Praktikum 9 vaate v_partiidpisi kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade v_isikudklubid on olemas?',
                name='v_partiidpisi',
                points=1,
            ),
            ViewTest(
                title='Kas veerg id on olemas?',
                name='v_partiidpisi',
                column_name='id',
                points=1,
            ),
            ViewTest(
                title='Kas veerg valge_mangija on olemas?',
                name='v_partiidpisi',
                column_name='valge_mangija',
                points=1,
            ),
            ViewTest(
                title='Kas veerg valge_punkt on olemas?',
                name='v_partiidpisi',
                column_name='valge_punkt',
                points=1,
            ),
            ViewTest(
                title='Kas veerg must_mangija on olemas?',
                name='v_partiidpisi',
                column_name='must_mangija',
                points=1,
            ),
            ViewTest(
                title='Kas veerg must_punkt on olemas?',
                name='v_partiidpisi',
                column_name='must_punkt',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='v_partiidpisi',
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas partiis 1 on valge ja musta mängijate nimed õigel kujul?',
                name='v_partiidpisi',
                column_name='COUNT(*)',
                where="id = 1 and valge_mangija = 'Katrin Kask' and must_mangija = 'Malle Maasikas'",
                expected_value=1,
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas partiis 61 valge mängija sai 1 punkti?',
                name='v_partiidpisi',
                column_name='round(valge_punkt,0)',
                where="id = 61 and valge_mangija = 'Jelena Pirn'",
                expected_value=1,
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas partiis 61 must mängija sai 0 punkti?',
                name='v_partiidpisi',
                column_name='round(must_punkt,0)',
                where="id = 61 and must_mangija = 'Henno Hiis'",
                expected_value=0,
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas partiis 83 saadi viigi eest 0.5 punkti?',
                name='v_partiidpisi',
                column_name='COUNT(*)',
                where="id = 83 and must_punkt = 0.5 and valge_punkt = 0.5",
                expected_value=1,
                isView=True,
                points=1,
            ),
        ],
    ),
    # 6; 20p - total 35
    ChecksLayer(
        title='Praktikum 9 vaate v_punktid kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade v_punktid on olemas?',
                name='v_punktid',
                points=1,
            ),
            ViewTest(
                title='Kas veerg partii on olemas?',
                name='v_punktid',
                column_name='partii',
                points=1,
            ),
            ViewTest(
                title='Kas veerg turniir on olemas?',
                name='v_punktid',
                column_name='turniir',
                points=1,
            ),
            ViewTest(
                title='Kas veerg mangija on olemas?',
                name='v_punktid',
                column_name='mangija',
                points=1,
            ),
            ViewTest(
                title='Kas veerg varv on olemas?',
                name='v_punktid',
                column_name='varv',
                points=1,
            ),
            ViewTest(
                title='Kas veerg punkt on olemas?',
                name='v_punktid',
                column_name='punkt',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='v_punktid',
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas mängija on V värvi?',
                name='v_punktid',
                column_name='varv',
                where="partii=51 and mangija=198",
                expected_value='V',
                isView=True,
                points=2,
            ),
            DataTest(
                title='Kas partii kaotaja sai 0 punkti?',
                name='v_punktid',
                column_name='round(punkt,0)',
                where="partii=51 and mangija=198",
                expected_value=0,
                isView=True,
                points=3,
            ),
            DataTest(
                title='Kas mängija on M värvi?',
                name='v_punktid',
                column_name='varv',
                where="partii=51 and mangija=82",
                expected_value='M',
                isView=True,
                points=2,
            ),
            DataTest(
                title='Kas partii võitja sai 1 punkti?',
                name='v_punktid',
                column_name='round(punkt,0)',
                where="partii=51 and mangija=82",
                expected_value=1,
                isView=True,
                points=3,
            ),
            DataTest(
                title='Kas viigi korral saadi 0.5 punkti?',
                name='v_punktid',
                column_name='round(punkt,1)',
                where="partii=54 and mangija=75",
                expected_value=0.5,
                isView=True,
                points=3,
            ),
        ],
    ),
    # 7; 25p -- total 60
    ChecksLayer(
        title='Praktikum 9 vaate v_edetabelid kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade v_edetabelid on olemas?',
                name='v_edetabelid',
                points=7,
            ),
            ViewTest(
                title='Kas veerg id on olemas?',
                name='v_edetabelid',
                column_name='id',
                points=1,
            ),
            ViewTest(
                title='Kas veerg mangija on olemas?',
                name='v_edetabelid',
                column_name='mangija',
                points=1,
            ),
            ViewTest(
                title='Kas veerg synniaeg on olemas?',
                name='v_edetabelid',
                column_name='synniaeg',
                points=1,
            ),
            ViewTest(
                title='Kas veerg ranking on olemas?',
                name='v_edetabelid',
                column_name='ranking',
                points=1,
            ),
            ViewTest(
                title='Kas veerg klubi on olemas?',
                name='v_edetabelid',
                column_name='klubi',
                points=1,
            ),
            ViewTest(
                title='Kas veerg turniir on olemas?',
                name='v_edetabelid',
                column_name='turniir',
                points=1,
            ),
            ViewTest(
                title='Kas veerg punkte on olemas?',
                name='v_edetabelid',
                column_name='punkte',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='v_edetabelid',
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas on turniiril 42 kõige suurem punktide arv õige?',
                name='v_edetabelid',
                column_name='round(MAX(punkte),0)',
                where='turniir=42',
                expected_value=7,
                isView=True,
                points=5,
            ),
            DataTest(
                title='Kas on turniiril 41 kõige väiksem punktide arv õige?',
                name='v_edetabelid',
                column_name='round(MIN(punkte),1)',
                where='turniir=41',
                expected_value=0.5,
                isView=True,
                points=5,
            ),
        ],
    ),
    # 10; 10p -- total 70p
    ChecksLayer(
        title='Praktikum 9 vaate mv_edetabelid kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade mv_edetabelid on olemas?',
                name='mv_edetabelid',
                isMaterialized=True,
                points=5,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='mv_edetabelid',
                isView=True,
                points=5,
            )
        ],
    ),
    # 11 ja 12; 20p -- total 90
    ChecksLayer(
        title='Praktikum 9 vaate v_klubi54 kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade v_klubi54 on olemas?',
                name='v_klubi54',
                points=5,
            ),
            ViewTest(
                title='Kas veerg eesnimi on olemas?',
                name='v_klubi54',
                column_name='eesnimi',
                points=1,
            ),
            ViewTest(
                title='Kas veerg perenimi on olemas?',
                name='v_klubi54',
                column_name='perenimi',
                points=1,
            ),
            ViewTest(
                title='Kas veerg synniaeg on olemas?',
                name='v_klubi54',
                column_name='synniaeg',
                points=1,
            ),
            ViewTest(
                title='Kas veerg ranking on olemas?',
                name='v_klubi54',
                column_name='ranking',
                points=1,
            ),
            ViewTest(
                title='Kas veerg klubi_id on olemas?',
                name='v_klubi54',
                column_name='klubi_id',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='v_klubi54',
                isView=True,
                points=5,
            ),
            # 12 insert
            DataTest(
                title='Kas Piibe Leht on lisatud vaate kaudu?',
                name='v_klubi54',
                column_name='COUNT(*)',
                where="eesnimi = 'Piibe' and perenimi = 'Leht'",
                expected_value=1,
                isView=True,
                points=5,
            ),
        ],
    ),
    # 13; 10p -- total 100
    ChecksLayer(
        title='Praktikum 9 vaate v_maletaht kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade v_maletaht on olemas?',
                name='v_maletaht',
                points=1,
            ),
            ViewTest(
                title='Kas veerg id on olemas?',
                name='v_maletaht',
                column_name='id',
                points=1,
            ),
            ViewTest(
                title='Kas veerg eesnimi on olemas?',
                name='v_maletaht',
                column_name='eesnimi',
                points=1,
            ),
            ViewTest(
                title='Kas veerg perenimi on olemas?',
                name='v_maletaht',
                column_name='perenimi',
                points=1,
            ),
            ViewTest(
                title='Kas veerg isikukood on olemas?',
                name='v_maletaht',
                column_name='isikukood',
                points=1,
            ),
            ViewTest(
                title='Kas veerg klubis on olemas?',
                name='v_maletaht',
                column_name='klubis',
                points=1,
            ),
            ViewTest(
                title='Kas veerg synniaeg on olemas?',
                name='v_maletaht',
                column_name='synniaeg',
                points=1,
            ),
            ViewTest(
                title='Kas veerg sugu on olemas?',
                name='v_maletaht',
                column_name='sugu',
                points=1,
            ),
            ViewTest(
                title='Kas veerg ranking on olemas?',
                name='v_maletaht',
                column_name='ranking',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='v_maletaht',
                column_name='COUNT(*)',
                expected_value=9,
                isView=True,
                points=1,
            )
        ],
    ),
    # Kodutöö 5 kontrollid
    # 25p
    ChecksLayer(
        title='Kodutöö 5 funktsiooni f_vanus kontrollid',
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
        title='Kodutöö 5 funktsiooni f_klubiranking kontrollid',
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
        title='Kodutöö 5 funktsiooni f_top10 kontrollid',
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
    # 25p
    ChecksLayer(
        title='Kodutöö 5 protseduuri sp_uus_turniir kontrollid',
        tests=[
            ProcedureTest(
                title='Kas on õige lõppkuupäev ühe päevasel turniiril?',
                name='sp_uus_turniir',
                arguments=['Haapsalu Meister', '02.02.2022', 1, 'Haapsalu'],
                number_of_parameters=4,
                pre_query="DELETE FROM turniirid WHERE nimi='Haapsalu Meister'",
                after_query="select * from turniirid where nimi = 'Haapsalu Meister' and (loppkuupaev = '02.02.2022' or loppkuupaev = '2022-02-22')",
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
                arguments=['Tartu Meister', '02.02.2022', 2, 'Tartu'],
                number_of_parameters=4,
                pre_query="DELETE FROM turniirid WHERE nimi='Tartu Meister'",
                after_query="select * from turniirid where nimi = 'Tartu Meister' and (loppkuupaev = '03.02.2022' or loppkuupaev = '2022-02-03')",
                points=12,
            ),
        ]
    ),
    # Praktikum 10
    # 1, 10p
    ChecksLayer(
        title='Praktikum 10 funktsiooni f_mangija_punktid_turniiril kontrollid',
        tests=[
            FunctionTest(
                title='Kas mängija punktid turniiril on õige?',
                name='f_mangija_punktid_turniiril',
                arguments=[92, 42],
                number_of_parameters=2,
                expected_value=5.5,
                points=10,
            ),
        ],
    ),
    # 2.1 5p
    ChecksLayer(
        title='Praktikum 10 funktsiooni f_nimi kontrollid',
        tests=[
            FunctionTest(
                title='Kas nimekuju on õige?',
                name='f_nimi',
                arguments=['test', 'kesk'],
                number_of_parameters=2,
                expected_value='kesk, test',
                points=5,
            ),
        ],
    ),
    # 2.2 5p
    ChecksLayer(
        title='Praktikum 10 funktsiooni f_klubisuurus kontrollid',
        tests=[
            FunctionTest(
                title='Kas klubisuurus on õige?',
                name='f_klubisuurus',
                arguments=[50],
                number_of_parameters=1,
                expected_value=9,
                points=5,
            ),
        ],
    ),
    # 3, 10p (30p)
    ChecksLayer(
        title='Praktikum 10 funktsiooni f_mangija_koormus kontrollid',
        tests=[
            FunctionTest(
                title='Kas mängija koormus on õige?',
                name='f_mangija_koormus',
                arguments=[73],
                number_of_parameters=1,
                expected_value=18,
                points=10,
            ),
        ],
    ),
    # 4, 10p (40p)
    ChecksLayer(
        title='Praktikum 10 funktsiooni f_mangija_voite_turniiril kontrollid',
        tests=[
            FunctionTest(
                title='Kas mängija võitude arv on õige?',
                name='f_mangija_voite_turniiril',
                arguments=[197, 43],
                number_of_parameters=2,
                expected_value=3,
                points=5,
            ),
            FunctionTest(
                title='Kas mängija võitude arv on 0?',
                name='f_mangija_voite_turniiril',
                arguments=[75, 44],
                number_of_parameters=2,
                expected_value=0,
                points=5,
            ),
        ],
    ),
    # 5.1, 10 (50p)
    ChecksLayer(
        title='Praktikum 10 funktsiooni f_mangija_viike_turniiril kontrollid',
        tests=[
            FunctionTest(
                title='Kas mängija viikide arv on õige?',
                name='f_mangija_viike_turniiril',
                arguments=[197, 43],
                number_of_parameters=2,
                expected_value=1,
                points=5,
            ),
            FunctionTest(
                title='Kas mängija viikide arv on 0?',
                name='f_mangija_viike_turniiril',
                arguments=[75, 44],
                number_of_parameters=2,
                expected_value=0,
                points=5,
            ),
        ],
    ),
    # 5.2, 10 (60p)
    ChecksLayer(
        title='Praktikum 10 funktsiooni f_mangija_kaotusi_turniiril kontrollid',
        tests=[
            FunctionTest(
                title='Kas mängija kaotuste arv on õige?',
                name='f_mangija_kaotusi_turniiril',
                arguments=[75, 44],
                number_of_parameters=2,
                expected_value=2,
                points=5,
            ),
            FunctionTest(
                title='Kas mängija kaotuste arv on 0?',
                name='f_mangija_kaotusi_turniiril',
                arguments=[197, 43],
                number_of_parameters=2,
                expected_value=0,
                points=5,
            ),
        ],
    ),
    # 6, 10p (70p)
    ChecksLayer(
        title='Praktikum 10 funktsiooni f_voit_viik_kaotus kontrollid',
        tests=[
            FunctionTest(
                title='Kas on õige tulemuste arv?',
                name='f_voit_viik_kaotus',
                arguments=[44],
                number_of_parameters=1,
                expected_count=63,
                points=4,
            ),
            FunctionTest(
                title='Kas mängijal on õige võitude arv?',
                name='f_voit_viik_kaotus',
                column_name='voite',
                where="id = 193",
                arguments=[44],
                number_of_parameters=1,
                expected_value=1,
                points=2,
            ),
            FunctionTest(
                title='Kas mängijal on õige viikide arv?',
                name='f_voit_viik_kaotus',
                column_name='viike',
                where="id = 193",
                arguments=[44],
                number_of_parameters=1,
                expected_value=1,
                points=2,
            ),
            FunctionTest(
                title='Kas mängijal on õige kaotuste arv?',
                name='f_voit_viik_kaotus',
                column_name='kaotusi',
                where="id = 193",
                arguments=[44],
                number_of_parameters=1,
                expected_value=0,
                points=2,
            ),
        ],
    ),
    # 7, 10p (80p)
    ChecksLayer(
        title='Praktikum 10 protseduuri sp_uus_isik kontrollid',
        tests=[
            ProcedureTest(
                title='Kas uus isik sai lisatud?',
                name='sp_uus_isik',
                arguments=['Uus', 'Isik', 51, 'm'],
                number_of_parameters=4,
                pre_query="DELETE FROM isikud WHERE eesnimi = 'Uus' and perenimi = 'Isik'",
                after_query="SELECT * FROM isikud WHERE eesnimi = 'Uus' and perenimi = 'Isik' and klubis = 51",
                points=8,
            ),
            DataTest(
                title='Kas klubiliikmete arv suurenes?',
                name='isikud',
                column_name='COUNT(*)',
                where="klubis=51",
                expected_value=5,
                points=2,
            ),
            ExecuteLayer("DELETE FROM isikud WHERE eesnimi = 'Uus' and pernimi = 'Isik'"),
        ],
    ),
    # 8, 10p (90p)
    ChecksLayer(
        title='Praktikum 10 funktsiooni f_klubiparimad kontrollid',
        tests=[
            FunctionTest(
                title='Kas on õige kirjete arv?',
                name='f_klubiparimad',
                arguments=['Areng'],
                number_of_parameters=1,
                expected_count=3,
                points=5,
            ),
            FunctionTest(
                title='Kas on õige mängija tulemus?',
                name='f_klubiparimad',
                column_name='ROUND(punktisumma,1)',
                arguments=['Areng'],
                number_of_parameters=1,
                where="isik = 'Põder, Priit'",
                expected_value=4.5,
                points=5,
            ),
        ],
    ),
    # 11, 10p, (100p)
    ChecksLayer(
        title='Praktikum 10 funktsiooni f_infopump kontrollid',
        tests=[
            FunctionTest(
                title='Kas on õige kirjete arv?',
                name='f_infopump',
                expected_count=108,
                points=10,
            ),
        ]
    ),
    # Kodutöö 6 kontrollid
    # 10p + 10p
    ChecksLayer(
        title='Kodutöö 6 indeksite kontrollid',
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
        title='Kodutöö 6 trigger tg_partiiaeg kontrollid',
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
            ExecuteLayer(
                f"INSERT INTO public.partiid VALUES (44,'2023-04-22 17:45:24.000','2023-03-22 17:45:24.000',{_user1},{_user2},2,0, {_partii_id})", ),
            DataTest(
                title='Kas testimiseks lisatud isikute partii lõpphetk on õige? Kui sul tuleb count = 0, siis sisestatud kirjel pole lopphetk NULL.',
                name='partiid',
                column_name='lopphetk',
                where=f"valge = {_user1} AND must = {_user2} and EXISTS(SELECT * FROM information_schema.triggers WHERE trigger_name = 'tg_partiiaeg')",
                expected_value='NULL',
                points=11,
            ),
        ],
    ),
    # 25p
    ChecksLayer(
        title='Kodutöö 6 trigger tg_klubi_olemasolu kontrollid',
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
    ),
    # Praktikum 11
    ChecksLayer(
        title='Praktikum 11 trigeri tg_ajakontroll kontrollid',
        tests=[
            TriggerTest(
                title='Kas on õige definitsioon tg_ajakontroll?',
                name='tg_ajakontroll',
                arguments=['UPDATE', 'INSERT'],
                action_timing='BEFORE',
                points=10,
            ),
        ]
    ),
    ChecksLayer(
        title='Praktikum 11 indeksi ix_nimed kontroll',
        tests=[
            IndexTest(
                title='Kas on olemas indeks ix_nimed?',
                name='ix_nimed',
                points=10,
            ),
        ]
    ),
    ChecksLayer(
        title='Praktikum 11 trigeri tg_riigid kontrollid',
        tests=[
            TriggerTest(
                title='Kas on õige definitsioon tg_riigid?',
                name='tg_riigid',
                arguments=['INSERT'],
                action_timing='BEFORE',
                points=10,
            ),
            ExecuteLayer("ALTER TABLE public.riigid DISABLE TRIGGER ALL"),
            ExecuteLayer("ALTER TABLE public.riigid ENABLE TRIGGER tg_riigid"),
            ExecuteLayer(f"DELETE FROM public.riigid WHERE id in (3000, 3001)"),
            ExecuteLayer(f"INSERT INTO public.riigid (id, nimi, pealinn) VALUES (3000,'Bulgaaria1','Sofia1')"),
            DataTest(
                title='Kas uue nimega riik lisati?',
                name='riigid',
                where="id=3000",
                should_exist=True,
                points=10,
            ),
            ExecuteLayer(f"INSERT INTO public.riigid (id, nimi, pealinn) VALUES (3001,'Bulgaaria1','Sofia1')"),
            DataTest(
                title='Kas sama nimega riiki ei lisatud?',
                name='riigid',
                where="id=3001",
                should_exist=False,
                points=10,
            ),
        ]
    ),
    ChecksLayer(
        title='Praktikum 11 trigeri tg_ajakontroll1 kontrollid',
        tests=[
            TriggerTest(
                title='Kas on õige definitsioon tg_ajakontroll1?',
                name='tg_ajakontroll1',
                arguments=['UPDATE', 'INSERT'],
                action_timing='BEFORE',
                points=10,
            ),
            ExecuteLayer("ALTER TABLE public.partiid DISABLE TRIGGER ALL"),
            ExecuteLayer("ALTER TABLE public.partiid ENABLE TRIGGER tg_ajakontroll1"),
            ExecuteLayer("ALTER TABLE public.isikud DISABLE TRIGGER ALL"),
            ExecuteLayer(f"DELETE FROM public.isikud WHERE id in ({_user1},{_user2})"),
            ExecuteLayer(f"INSERT INTO public.isikud (id, eesnimi, perenimi) VALUES ({_user1},'Man', 'Ka')"),
            ExecuteLayer(f"INSERT INTO public.isikud (id, eesnimi, perenimi) VALUES ({_user2},'Kan', 'Ma')"),
            ExecuteLayer(
                f"INSERT INTO public.partiid VALUES (44,'2023-03-22 17:45:24.000','2023-03-22 17:47:24.000',{_user1},{_user2},2,0, {_partii_id})", ),
            DataTest(
                title='Kas partii lisamine õnnestus?',
                name='partiid',
                where=f"id={_partii_id}",
                points=10,
            ),
            ExecuteLayer(
                f"INSERT INTO partiid (turniir, algushetk, valge, must, valge_tulemus, musta_tulemus) VALUES (41, '2005-01-12 08:05:00.000', 73, 92, 1, 1, {_partii_id + 1})", ),
            DataTest(
                title='Kas partii lisamine ebaõnnestus?',
                name='partiid',
                where=f"id={_partii_id + 1}",
                points=10,
                should_exist=False,
            ),
        ]
    ),
    ChecksLayer(
        title='Praktikum 11 trigeri tg_kustuta_klubi kontrollid',
        tests=[
            TriggerTest(
                title='Kas on õige definitsioon tg_kustuta_klubi?',
                name='tg_kustuta_klubi',
                arguments=['DELETE'],
                action_timing='AFTER',
                points=20,
            ),
            ExecuteLayer("ALTER TABLE public.klubid DISABLE TRIGGER ALL"),
            ExecuteLayer("ALTER TABLE public.klubid ENABLE TRIGGER tg_kustuta_klubi"),
            ExecuteLayer("ALTER TABLE public.asulad DISABLE TRIGGER ALL"),
            ExecuteLayer(f"DELETE FROM public.asulad WHERE id in ({_asula_id})"),
            ExecuteLayer(f"DELETE FROM public.klubid WHERE id in ({_klubi_id})"),
            ExecuteLayer(f"INSERT INTO public.asulad VALUES ({_asula_id},{_asula_nimi})"),
            ExecuteLayer(f"INSERT INTO public.klubid (id, nimi, asula) VALUES ({_klubi_id},{_klubi_nimi},{_asula_id}"),
            ExecuteLayer(f"DELETE FROM klubid WHERE nimi={_klubi_nimi}"),
            DataTest(
                title='Kas klubi kustutamisel kustus ka asula?',
                name='asulad',
                where=f"nimi='{_asula_nimi}'",
                should_exist=False,
                points=1,
            )
        ]
    ),
    ChecksLayer(
        title='Praktikum 11 trigeri tg_partiiaeg1 kontrollid',
        tests=[
            TriggerTest(
                title='Kas on õige definitsioon tg_partiiaeg1?',
                name='tg_partiiaeg1',
                arguments=['UPDATE', 'INSERT'],
                action_timing='BEFORE',
                points=12,
            ),
            ExecuteLayer("ALTER TABLE public.partiid DISABLE TRIGGER ALL"),
            ExecuteLayer("ALTER TABLE public.partiid ENABLE TRIGGER tg_partiiaeg1"),
            ExecuteLayer("ALTER TABLE public.isikud DISABLE TRIGGER ALL"),
            ExecuteLayer(f"DELETE FROM public.isikud WHERE id in ({_user1},{_user2})"),
            ExecuteLayer(f"INSERT INTO public.isikud (id, eesnimi, perenimi) VALUES ({_user1},'Man', 'Ka')"),
            ExecuteLayer(f"INSERT INTO public.isikud (id, eesnimi, perenimi) VALUES ({_user2},'Kan', 'Ma')"),
            ExecuteLayer(
                f"INSERT INTO Partiid(turniir, algushetk, valge, must, id) VALUES (41, '2005-01-22 08:04', {_user1},{_user2},{_partii_id + 2})"),
            DataTest(
                title='Kas partii lisamine ebaõnnestus, kui algusaeg enne turniiri?',
                name='partiid',
                where=f"id={_partii_id + 2}",
                points=2,
                should_exist=False,
            ),
            ExecuteLayer(
                f"INSERT INTO Partiid(turniir, algushetk, valge, must, id) VALUES (41, '2005-01-10 08:04', {_user1},{_user2},{_partii_id + 3})"),
            DataTest(
                title='Kas partii lisamine ebaõnnestus, kui algusaeg peale turniiri?',
                name='partiid',
                where=f"id={_partii_id + 3}",
                points=2,
                should_exist=False,
            ),
            ExecuteLayer(
                f"INSERT INTO Partiid(turniir, algushetk, lopphetk, valge, must, id) VALUES (41, '2005-01-12 08:04', '2005-01-22 09:10', {_user1},{_user2},{_partii_id + 4})"),
            DataTest(
                title='Kas partii lisamine ebaõnnestus, kui lõppaeg enne turniiri?',
                name='partiid',
                where=f"id={_partii_id + 4}",
                points=2,
                should_exist=False,
            ),
            ExecuteLayer(
                f"INSERT INTO Partiid(turniir, algushetk, lopphetk, valge, must, id) VALUES (41, '2005-01-12 08:04', '2005-01-01 09:10', {_user1},{_user2},{_partii_id + 5})"),
            DataTest(
                title='Kas partii lisamine ebaõnnestus, kui lõppaeg peale turniiri?',
                name='partiid',
                where=f"id={_partii_id + 5}",
                points=2,
                should_exist=False,
            ),
        ]
    ),
]