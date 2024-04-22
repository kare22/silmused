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
# Praktikum 3
tests = [
    # Ülesanne 1, 14; 10p
    ChecksLayer(
        title='Tabeli Turniirid kontrollid',
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
            StructureTest(
                title='Kas veerg asukoht on olemas?',
                name='turniirid',
                column_name='asukoht',
                points=3,
                ),
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
        title='Tabeli Isikud kontrollid',
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
                title='Kas on lisatud 5 liiget klubwwisse Osav Oda?',
                name='isikud',
                column_name='COUNT(*)',
                where="klubis = (select id from klubid where nimi = 'Osav Oda')",
                expected_value=5,
                points=7,
            ),
        ]
    ),
    # 9; 15p
    ChecksLayer(
        title='Õ tähtede vahetamise kontrollid',
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
        title='Tabeli Partiid kontrollid',
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
        title='Tabeli Klubid kontrollid',
        tests=[
            # 7
            StructureTest(
                title='Kas veeru asukoha väärtuse maksimum suurus on õige?',
                name='klubid',
                column_name='asukoht',
                expected_character_maximum_length=100,
                points=5,
            ),
            # 11
            DataTest(
                title='Kas klubi osav oda on olemas?',
                name='klubid',
                where="nimi = 'Osav Oda'",
                points=10,
            ),
            # 16
            DataTest(
                title='Kas klubi Valge mask asukoht on Valga?',
                name='klubid',
                column_name='asukoht',
                where="nimi = 'Valge Mask'",
                expected_value='Valga',
                points=5,
            ),
        ]
    ),
]

# Praktikum 4

tests = [
    # Ülesanne 1, 4, 40p
    ChecksLayer(
        title='Tabeli Asulad kontrollid',
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
            #4
            DataTest(
                title='Kas tabelis asulad on andmed olemas?',
                name='asulad',
                points=15,
            ),
        ]
    ),
    # Ülesanne 2, 3, 20p
    ChecksLayer(
        title='Tabeli Riigid kontrollid',
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
            #3
            DataTest(
                title='Kas tabelis riigid on andmed olemas?',
                name='riigid',
                points=5,
            ),
        ]
    ),
    # Ülesanne 5, 6, 7, 9, 40p
    ChecksLayer(
        title='Tabeli Klubid kontrollid',
        tests=[
            #5
            StructureTest(
                title='Kas veerg asula on olemas?',
                name='klubid',
                column_name='asula',
                points=10,
            ),
            #6
            DataTest(
                title='Kas veerus asula on andmed olemas?',
                name='klubid',
                column_name='asula',
                points=10,
            ),
            #7
            ConstraintTest(
                title='Kas tabelis on välisvõti olemas?',
                name='klubid',
                constraint_type='FOREIGN KEY',
                points=10,
            ),
            #9
            StructureTest(
                title='Kas veerg asukoht on kustutatud?',
                name='klubid',
                column_name='asukoht',
                should_exist=False,
                points=5,
            ),
            #9
            StructureTest(
                title='Kas veerg toimumiskoht on kustutatud?',
                name='klubid',
                column_name='toimumiskoht',
                should_exist=False,
                points=5,
            ),

        ]
    ),
]
"""
"""
# Praktikum 8 100p
tests = [
    # 4p
    ChecksLayer(
        title='Tabeli Institutes kontrollid',
        tests=[
            StructureTest(
                title='Kas tabel institutes on olemas?',
                name='institutes',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='institutes',
                points=1,
            ),
            ConstraintTest(
                title='Kas välisvõti on olemas?',
                name='institutes',
                constraint_type='FOREIGN KEY',
                points=1,
            ),
            ConstraintTest(
                title='Kas välisvõti on olemas?',
                name='institutes',
                constraint_type='FOREIGN KEY',
                points=1,
            ),
        ]
    ),
    # 5p
    ChecksLayer(
        title='Tabeli Persons kontrollid',
        tests=[
            StructureTest(
                title='Kas tabel persons on olemas?',
                name='persons',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='persons',
                points=1,
            ),
            ConstraintTest(
                title='Kas välisvõti on olemas?',
                name='persons',
                constraint_type='FOREIGN KEY',
                points=3,
            ),
        ]
    ),
    # 4p
    ChecksLayer(
        title='Tabeli Registrations kontrollid',
        tests=[
            StructureTest(
                title='Kas tabel registrations on olemas?',
                name='registrations',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='registrations',
                points=1,
            ),
            ConstraintTest(
                title='Kas välisvõti on olemas?',
                name='registrations',
                constraint_type='FOREIGN KEY',
                points=1,
            ),
            ConstraintTest(
                title='Kas välisvõti on olemas?',
                name='registrations',
                constraint_type='FOREIGN KEY',
                points=1,
            ),
        ]
    ),
    # 3p
    ChecksLayer(
        title='Tabeli Lecturers kontrollid',
        tests=[
            StructureTest(
                title='Kas tabel lecturers  on olemas?',
                name='lecturers',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='lecturers',
                points=1,
            ),
            ConstraintTest(
                title='Kas välisvõti on olemas?',
                name='lecturers',
                constraint_type='FOREIGN KEY',
                points=1,
            ),
        ]
    ),
    # 5p
    ChecksLayer(
        title='Tabeli Courses kontrollid',
        tests=[
            StructureTest(
                title='Kas tabel courses on olemas?',
                name='courses',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='courses',
                points=1,
            ),
            ConstraintTest(
                title='Kas välisvõti on olemas?',
                name='courses',
                constraint_type='FOREIGN KEY',
                points=3,
            ),
        ],
    ),
    # 2p
    ChecksLayer(
        title='Vaate v_oigusteaduskonna_inimesed kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade v_oigusteaduskonna_inimesed on olemas?',
                name='v_oigusteaduskonna_inimesed',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='v_oigusteaduskonna_inimesed',
                column_name='COUNT(*)',
                expected_value=28,
                isView=True,
                points=1,
            ),
        ],
    ),
    # 2p
    ChecksLayer(
        title='Vaate v_persons_institute kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade v_persons_institute on olemas?',
                name='v_persons_institute',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='v_persons_institute',
                column_name='COUNT(*)',
                expected_value=300,
                isView=True,
                points=1,
            ),
        ],
    ),
    # 3p
    ChecksLayer(
        title='Vaate v_institute_deans kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade v_institute_deans on olemas?',
                name='v_institute_deans',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='v_institute_deans',
                column_name='COUNT(*)',
                expected_value=10,
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas Usuteaduskonna vicedean on puudu?',
                name='v_institute_deans',
                column_name='vicedeanname',
                where="institutename='Usuteaduskond'",
                expected_value='None',
                isView=True,
                points=1,
            ),
        ],
    ),
    # 4p
    ChecksLayer(
        title='Vaate v_top20students kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade v_top20students on olemas?',
                name='v_top20students',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='v_top20students',
                column_name='COUNT(*)',
                expected_value=20,
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas Henry Lesmenti eksami keskmine hinne on 4?',
                name='v_top20students',
                column_name='ROUND(averagegrade,0)',
                where="firstname='Henry' AND lastname = 'Lesment'",
                expected_value='4',
                isView=True,
                points=1,
            ),
            DataTest(
                title='Kas Mart Mustika eksami keskmine hinne on 3.8?',
                name='v_top20students',
                column_name='ROUND(averagegrade,1)',
                where="firstname='Mart' AND lastname = 'Mustikas'",
                expected_value='3.8',
                isView=True,
                points=1,
            ),
        ],
    ),
    # 2p - total 34p
    ChecksLayer(
        title='Kursus Sissejuhatus informaatikasse',
        tests=[
            DataTest(
                title='Kas kursus Sissejuhatus informaatikasse on olemas?',
                name='courses',
                column_name='COUNT(*)',
                where="name='Sissejuhatus informaatikasse'",
                expected_value=1,
                points=1,
            ),
            DataTest(
                title='Kas kursusel Sissejuhatus informaatikasse on tudengid olemas?',
                name='registrations',
                column_name='COUNT(*)',
                where="courseid=101",
                expected_value=15,
                points=1,
            ),
        ],
    ),
    # 13p
    ChecksLayer(
        title='Vaate v_persons_atleast_4eap kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade v_persons_atleast_4eap on olemas?',
                name='v_persons_atleast_4eap',
                points=5,
            ),
            ViewTest(
                title='Kas veerg FirstName on olemas?',
                name='v_persons_atleast_4eap',
                column_name='firstname',
                points=1,
            ),
            ViewTest(
                title='Kas veerg LastName on olemas?',
                name='v_persons_atleast_4eap',
                column_name='lastname',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='v_persons_atleast_4eap',
                column_name='COUNT(*)',
                expected_value=135,
                isView=True,
                points=6,
            ),
        ],
    ),
    # 23p
    ChecksLayer(
        title='Vaate v_countOfA kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade v_countOfA on olemas?',
                name='v_countofa',
                points=5,
            ),
            ViewTest(
                title='Kas veerg FirstName on olemas?',
                name='v_countofa',
                column_name='firstname',
                points=1,
            ),
            ViewTest(
                title='Kas veerg LastName on olemas?',
                name='v_countofa',
                column_name='lastname',
                points=1,
            ),
            ViewTest(
                title='Kas veerg CountOfA on olemas?',
                name='v_countofa',
                column_name='countofa',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='v_countofa',
                column_name='COUNT(*)',
                expected_value=119,
                isView=True,
                points=5,
            ),
            DataTest(
                title='Kas suurim A-de kogus on 5?',
                name='v_countofa',
                column_name='MAX(countofa)',
                expected_value=5,
                isView=True,
                points=5,
            ),
            DataTest(
                title='Kas väikseim A-de kogus on 1?',
                name='v_countofa',
                column_name='MIN(countofa)',
                expected_value=1,
                isView=True,
                points=5,
            ),
        ],
    ),
    # 30p
    ChecksLayer(
        title='Vaate v_top40A kontrollid',
        tests=[
            ViewTest(
                title='Kas vaade v_top40A on olemas?',
                name='v_top40a',
                points=10,
            ),
            ViewTest(
                title='Kas veerg FirstName on olemas?',
                name='v_top40a',
                column_name='firstname',
                points=1,
            ),
            ViewTest(
                title='Kas veerg LastName on olemas?',
                name='v_top40a',
                column_name='lastname',
                points=1,
            ),
            ViewTest(
                title='Kas veerg CountOfA on olemas?',
                name='v_top40a',
                column_name='countofa',
                points=1,
            ),
            DataTest(
                title='Kas andmed on olemas?',
                name='v_top40a',
                column_name='COUNT(*)',
                expected_value=40,
                isView=True,
                points=2,
            ),
            DataTest(
                title='Kas suurim A-de kogus on 6?',
                name='v_top40a',
                column_name='MAX(countofa)',
                expected_value=6,
                isView=True,
                points=10,
            ),
            DataTest(
                title='Kas väikseim A-de kogus on 4?',
                name='v_top40a',
                column_name='MIN(countofa)',
                expected_value=4,
                isView=True,
                points=5,
            ),
        ],
    ),
]"""
"""
# Praktikum 9 100p
tests = [
    # 1; 2p
    ChecksLayer(
        title='Vaate v_isikudklubid kontrollid',
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
        title='Vaate v_partiid kontrollid',
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
        title='Vaate v_partiidpisi kontrollid',
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
        title='Vaate v_punktid kontrollid',
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
        title='Vaate v_edetabelid kontrollid',
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
        title='Vaate mv_edetabelid kontrollid',
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
        title='Vaate v_klubi54 kontrollid',
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
            #12 insert
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
        title='Vaate v_maletaht kontrollid',
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
]
"""
"""
tests = [
    # 1, 10p
    ChecksLayer(
        title='Funktsiooni f_mangija_punktid_turniiril kontrollid',
        tests=[
            FunctionTest(
                title='Kas mängija punktid turniiril on õige?',
                name='f_mangija_punktid_turniiril',
                arguments=[92,42],
                number_of_parameters=2,
                expected_value=5.5,
                points=10,
            ),
        ],
    ),
    # 2.1 5p
    ChecksLayer(
        title='Funktsiooni f_nimi kontrollid',
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
        title='Funktsiooni f_klubisuurus kontrollid',
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
        title='Funktsiooni f_mangija_koormus kontrollid',
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
        title='Funktsiooni f_mangija_voite_turniiril kontrollid',
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
        title='Funktsiooni f_mangija_viike_turniiril kontrollid',
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
        title='Funktsiooni f_mangija_kaotusi_turniiril kontrollid',
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
        title='Funktsiooni f_voit_viik_kaotus kontrollid',
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
        title='Protseduuri sp_uus_isik kontrollid',
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
        title='Funktsiooni f_klubiparimad kontrollid',
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
        title='Funktsiooni f_infopump kontrollid',
        tests=[
            FunctionTest(
                title='Kas on õige kirjete arv?',
                name='f_infopump',
                expected_count=105,
                points=10,
            ),
        ]
    ),
]
"""
_user1 = 123456
_user2 = 123457
_partii_id = 123123
_asula_id = 200
_asula_nimi='Test_asula'
_klubi_id = 201
_klubi_nimi = 'Klubi kustutamiseks'
tests = [
    ChecksLayer(
        title='Trigeri tg_ajakontroll kontrollid',
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
        title='Indeksi ix_nimed kontroll',
        tests=[
            IndexTest(
                title='Kas on olemas indeks ix_nimed?',
                name='ix_nimed',
                points=10,
            ),
        ]
    ),
    ChecksLayer(
        title='Trigeri tg_riigid kontrollid',
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
            ExecuteLayer(f"INSERT INTO public.riigid (id, nimi, pealinn) VALUES (3001,'Bulgaaria','Sofia2')"),

            DataTest(
                title='Kas uue nimega riik lisati?',
                name='riigid',
                where="id=3000",
                should_exist=True,
                points=10,
            ),
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
        title='Trigeri tg_ajakontroll1 kontrollid',
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
            ExecuteLayer(f"DELETE FROM public.partiid where id in ({_partii_id},{_partii_id+1})"),
            ExecuteLayer(f"INSERT INTO public.isikud (id, eesnimi, perenimi) VALUES ({_user1},'Man', 'Ka')"),
            ExecuteLayer(f"INSERT INTO public.isikud (id, eesnimi, perenimi) VALUES ({_user2},'Kan', 'Ma')"),
            ExecuteLayer(f"INSERT INTO public.partiid VALUES (44,'2023-03-22 17:45:24.000','2023-03-22 17:47:24.000',{_user1},{_user2},2,0, {_partii_id})", ),
            ExecuteLayer(f"INSERT INTO partiid (turniir, algushetk, valge, must, valge_tulemus, musta_tulemus) VALUES (41, '2005-01-12 08:05:00.000', 73, 92, 1, 1, {_partii_id+1})", ),
            DataTest(
                title='Kas partii lisamine õnnestus?',
                name='partiid',
                where=f"id={_partii_id}",
                points=10,
            ),
            DataTest(
                title='Kas partii lisamine ebaõnnestus?',
                name='partiid',
                where=f"id={_partii_id+1}",
                points=10,
                should_exist=False,
            ),
        ]
    ),
    ChecksLayer(
        title='Trigeri tg_kustuta_klubi kontrollid',
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
        title='Trigeri tg_partiiaeg1 kontrollid',
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
            ExecuteLayer(f"INSERT INTO Partiid(turniir, algushetk, valge, must, id) VALUES (41, '2005-01-22 08:04', {_user1},{_user2},{_partii_id+2})"),
            ExecuteLayer(f"INSERT INTO Partiid(turniir, algushetk, valge, must, id) VALUES (41, '2005-01-10 08:04', {_user1},{_user2},{_partii_id+3})"),
            ExecuteLayer(f"INSERT INTO Partiid(turniir, algushetk, lopphetk, valge, must, id) VALUES (41, '2005-01-12 08:04', '2005-01-22 09:10', {_user1},{_user2},{_partii_id+4})"),
            ExecuteLayer(f"INSERT INTO Partiid(turniir, algushetk, lopphetk, valge, must, id) VALUES (41, '2005-01-12 08:04', '2005-01-01 09:10', {_user1},{_user2},{_partii_id+5})"),
            DataTest(
                title='Kas partii lisamine ebaõnnestus, kui algusaeg enne turniiri?',
                name='partiid',
                where=f"id={_partii_id+2}",
                points=2,
                should_exist=False,
            ),
            DataTest(
                title='Kas partii lisamine ebaõnnestus, kui algusaeg peale turniiri?',
                name='partiid',
                where=f"id={_partii_id+3}",
                points=2,
                should_exist=False,
            ),
            DataTest(
                title='Kas partii lisamine ebaõnnestus, kui lõppaeg enne turniiri?',
                name='partiid',
                where=f"id={_partii_id+4}",
                points=2,
                should_exist=False,
            ),
            DataTest(
                title='Kas partii lisamine ebaõnnestus, kui lõppaeg peale turniiri?',
                name='partiid',
                where=f"id={_partii_id+5}",
                points=2,
                should_exist=False,
            ),
        ]
    ),
]