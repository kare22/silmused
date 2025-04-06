querys = {
    #"k1_1": "select eesnimi, perenimi from isikud order by synniaeg desc limit 5;",
    #"k1_2": "select eesnimi, perenimi, sugu, extract(year from age(current_date, synniaeg)) as vanus from isikud where perenimi like '%ets%';",
    #"k1_3": 'select round(ranking,-2) as "ränkingu klass", count(ranking) as arv from isikud group by "ränkingu klass" having count(ranking) > 5 order by count(ranking) desc;',
    #"k1_4": 'select extract(month from synniaeg) as "sünnikuu number",count(*) as arv from isikud where sugu='m' and left(eesnimi,2)=left(perenimi,2) group by "sünnikuu number" having count(*) > 1 order by arv;',
    #"k2_1": "select klubid.nimi from klubid, isikud, partiid where klubid.id = isikud.klubi and isikud.id = partiid.valge group by klubid.nimi having avg(partiid.valge_tulemus) > (select avg(partiid.valge_tulemus) from partiid, isikud, klubid where isikud.id = partiid.valge and klubid.nimi = 'Maletäht' and klubid.id = isikud.klubi );",
    "k2_3": "select * from isikud",
    #"k2_2": "select distinct klubid.nimi from isikud join partiid on isikud.id = partiid.must join klubid on isikud.klubi = klubid.id group by klubid.nimi, isikud.id having count(isikud.id) = 1;",
    #"k2_3": 'select eesnimi, perenimi, avg(tulemus) as "keskmine tulemus", nupu_varv as "nupu värv" from ( select eesnimi, perenimi, valge_tulemus as tulemus, 'valge' as nupu_varv from isikud left join partiid on isikud.id = partiid.valge union all select eesnimi, perenimi, must_tulemus as tulemus, 'must' as nupu_varv from isikud left join partiid on isikud.id = partiid.must ) group by eesnimi, perenimi, nupu_varv order by eesnimi, perenimi, avg(tulemus) desc;',
    #"k3_7": 'select a.nimi, count(k.asula) as "klubide arv" from asulad a left join klubid k on k.asula = a.id group by a.nimi order by 2 desc;',
    #"k3_8": "select distinct a.nimi from isikud i join partiid p on p.valge = i.id and p.valge_tulemus = 2 join turniirid t on p.turniir = t.id join asulad a on t.asula = a.id where i.perenimi = 'Kalamees';",
}

