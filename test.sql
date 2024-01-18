--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

-- Started on 2024-01-13 13:29:11

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA public;


--
-- TOC entry 4952 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- TOC entry 242 (class 1255 OID 17218)
-- Name: f_ajakontroll(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_ajakontroll() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
DELETE FROM partiid p WHERE EXISTS (
SELECT * FROM partiid q
WHERE p.algushetk>= q.algushetk AND
p.algushetk <= q.lopphetk AND p.id <> q.id AND
(p.valge = q.valge OR p.valge=q.must OR p.must=q.valge
OR p.must=q.must) AND q.turniir = p.turniir);
RETURN NULL;
END;
$$;


--
-- TOC entry 243 (class 1255 OID 17219)
-- Name: f_ajakontroll1(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_ajakontroll1() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    m_id integer;
BEGIN
    SELECT COUNT(*) INTO m_id FROM partiid p 
    WHERE NEW.algushetk >= p.algushetk AND NEW.algushetk <= p.lopphetk AND
    (NEW.valge = p.valge OR NEW.valge = p.must OR NEW.must = p.valge OR NEW.must = p.must);

    IF m_id > 0 THEN
        RAISE EXCEPTION 'See mängija mängib juba sel ajal!';
    ELSE
        RAISE NOTICE 'Partii lisatud!';
        RETURN NEW;
    END IF;
END;
$$;


--
-- TOC entry 244 (class 1255 OID 17220)
-- Name: f_klubi_id(text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_klubi_id(in_klubi_nimi text) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    klub_id integer;
BEGIN
    SELECT id INTO klub_id
    FROM klubid
    WHERE nimi = in_klubi_nimi;

    RETURN klub_id;
END;
$$;


--
-- TOC entry 249 (class 1255 OID 17221)
-- Name: f_klubiparimad(text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_klubiparimad(in_klubi_nimi text) RETURNS TABLE(nimi text, "kuupäev" timestamp with time zone)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT CONCAT_WS(' ', i.perenimi, i.eesnimi) AS nimi, now() AS kuupäev
    FROM isikud i
    INNER JOIN (
        SELECT m.mangija, SUM(m.punktid) AS summa
        FROM (
            SELECT valge AS mangija, valge_tulemus AS punktid
            FROM partiid
            UNION ALL
            SELECT must AS mangija, must_tulemus AS punktid
            FROM partiid
        ) m
         
        GROUP BY m.mangija
        ORDER BY summa DESC
        LIMIT 3
    ) t ON i.id = t.mangija
    WHERE i.klubi = f_klubi_id(in_klubi_nimi);
END;
$$;


--
-- TOC entry 256 (class 1255 OID 17222)
-- Name: f_klubiranking(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_klubiranking(a_id integer) RETURNS numeric
    LANGUAGE sql
    AS $$
   SELECT ROUND(AVG(isikud.ranking), 1) FROM isikud 
   WHERE isikud.klubi = a_id;
$$;


--
-- TOC entry 257 (class 1255 OID 17223)
-- Name: f_klubisuurus(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_klubisuurus(a_id integer) RETURNS integer
    LANGUAGE sql
    AS $$ SELECT count(isikud.id) FROM isikud RIGHT JOIN klubid ON isikud.klubi=klubid.id
WHERE klubid.id=a_id; $$;


--
-- TOC entry 259 (class 1255 OID 17224)
-- Name: f_kontrolli_klubi(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_kontrolli_klubi() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    klubi_id INTEGER;
BEGIN
    SELECT id INTO klubi_id FROM klubid WHERE nimi = 'Klubitud';
    IF NEW.klubi IS NULL THEN
        UPDATE isikud SET klubi = klubi_id WHERE id = NEW.id;
    END IF;
    RETURN NEW;
END;
$$;


--
-- TOC entry 260 (class 1255 OID 17225)
-- Name: f_kontrolli_klubi_asulat(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_kontrolli_klubi_asulat() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM klubid k 
        JOIN asulad a ON k.asula = a.id 
        WHERE k.asula = OLD.asula
    ) AND NOT EXISTS (
        SELECT 1 
        FROM turniirid t
        join asulad a on t.toimumiskoht = a.nimi 
        where a.id = old.asula
    ) THEN
        DELETE FROM asulad WHERE id = OLD.asula;
    END IF;
    RETURN NULL;
END;
$$;


--
-- TOC entry 261 (class 1255 OID 17226)
-- Name: f_lisa_riik(text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_lisa_riik(in_riik text) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
        INSERT INTO riigid (nimi) VALUES (in_riik);
    
END;
$$;


--
-- TOC entry 262 (class 1255 OID 17227)
-- Name: f_lisa_riik(text, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_lisa_riik(in_riik text, in_rahvaarv integer) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    
    
    INSERT INTO riigid (nimi, rahvaarv) VALUES (in_riik, in_rahvaarv);
    
    
    RAISE NOTICE 'Lisati uus riik: %', in_riik;
END;
$$;


--
-- TOC entry 263 (class 1255 OID 17228)
-- Name: f_mangija_kaotusi_turniiril(integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_mangija_kaotusi_turniiril(m_id integer, t_id integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    kaotusi integer;
BEGIN
    SELECT COUNT(*) INTO kaotusi
    FROM partiid
    WHERE turniir = t_id
        AND (
            (valge = m_id AND valge_tulemus < must_tulemus) OR
            (must = m_id AND must_tulemus < valge_tulemus)
        );

    RETURN kaotusi;
END;
$$;


--
-- TOC entry 264 (class 1255 OID 17229)
-- Name: f_mangija_koormus(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_mangija_koormus(mangija_id integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    mangu_count integer := 0;
BEGIN
    SELECT COUNT(*) INTO mangu_count 
    FROM partiid 
    WHERE valge = mangija_id OR must = mangija_id;
    
    RETURN mangu_count;
END;
$$;


--
-- TOC entry 265 (class 1255 OID 17230)
-- Name: f_mangija_viike_turniiril(integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_mangija_viike_turniiril(m_id integer, t_id integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    viike integer;
BEGIN
    SELECT COUNT(*) INTO viike
    FROM partiid
    WHERE turniir = t_id
        AND (
            (valge = m_id AND valge_tulemus = must_tulemus) OR
            (must = m_id AND must_tulemus = valge_tulemus)
        );

    RETURN viike;
END;
$$;


--
-- TOC entry 266 (class 1255 OID 17231)
-- Name: f_mangija_voite_turniiril(integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_mangija_voite_turniiril(m_id integer, t_id integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    voite integer;
BEGIN
    SELECT COUNT(*) INTO voite
    FROM partiid
    WHERE turniir = t_id
        AND (
            (valge = m_id AND valge_tulemus > must_tulemus) OR
            (must = m_id AND must_tulemus > valge_tulemus)
        );

    RETURN voite;
END;
$$;


--
-- TOC entry 267 (class 1255 OID 17232)
-- Name: f_nimi(character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_nimi(a_e character varying, a_p character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
DECLARE nimi varchar(202);
    BEGIN
        nimi := a_p||', '|| a_e;
        RETURN nimi;
    END;
$$;


--
-- TOC entry 268 (class 1255 OID 17233)
-- Name: f_partiiaeg_kontroll(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_partiiaeg_kontroll() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.lopphetk IS NOT NULL AND NEW.lopphetk <= NEW.algushetk THEN
        NEW.lopphetk := NULL;
        RAISE NOTICE 'Lõppaega ei sisestatud, sest see oli varasem kui algusaeg!';
    END IF;
    RETURN NEW;
END;
$$;


--
-- TOC entry 269 (class 1255 OID 17234)
-- Name: f_riigi_kontroll(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_riigi_kontroll() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM riigid
        WHERE nimi = NEW.nimi
    ) THEN
        RAISE notice 'Riik "%" on juba tabelis "riigid"', NEW.nimi;
    ELSE
        RETURN NEW;
    END IF;
END;
$$;


--
-- TOC entry 270 (class 1255 OID 17235)
-- Name: f_riigi_lisamine(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_riigi_lisamine() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM riigid
        WHERE nimetus = NEW.nimetus
    ) THEN
        RAISE EXCEPTION 'Riik "%s" on juba tabelis "riigid"', NEW.nimetus;
    ELSE
        RETURN NEW;
    END IF;
END;
$$;


--
-- TOC entry 271 (class 1255 OID 17236)
-- Name: f_top10(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_top10(in_turniiri_id integer) RETURNS TABLE(nimi text, punkte numeric)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT m.mangija AS mangija, m.punkte
    FROM v_edetabelid m
    WHERE m.turniir = in_turniiri_id
    ORDER BY m.punkte DESC
    LIMIT 10;
END;
$$;


--
-- TOC entry 272 (class 1255 OID 17237)
-- Name: f_vanus(date); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_vanus(synnikuupaev date) RETURNS integer
    LANGUAGE sql
    AS $$
  SELECT EXTRACT(YEAR FROM age(current_date, synnikuupaev))::INTEGER;
$$;


--
-- TOC entry 240 (class 1255 OID 17238)
-- Name: f_voit_viik_kaotus(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION f_voit_viik_kaotus(t_id integer) RETURNS TABLE(id integer, eesnimi character varying, perenimi character varying, voite integer, viike integer, kaotusi integer, kuupaev date)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT
        i.id,
        i.eesnimi,
        i.perenimi,
        f_mangija_voite_turniiril(i.id, t_id) AS voite,
        f_mangija_viike_turniiril(i.id, t_id) AS viike,
        f_mangija_kaotusi_turniiril(i.id, t_id) AS kaotusi,
        CURRENT_DATE AS kuupaev
    FROM
        isikud i
    JOIN
        partiid p ON i.id = p.valge OR i.id = p.must
    WHERE
        p.turniir = t_id
    GROUP BY
        i.id,
        i.eesnimi,
        i.perenimi;
END;
$$;


--
-- TOC entry 241 (class 1255 OID 17239)
-- Name: sp_uus_isik(text, text, integer); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE sp_uus_isik(IN in_eesnimi text, IN in_perenimi text, IN in_klubi_id integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO isikud (eesnimi, perenimi, klubi)
    VALUES (in_eesnimi, in_perenimi, in_klubi_id);
END;
$$;


--
-- TOC entry 273 (class 1255 OID 17240)
-- Name: sp_uus_turniir(text, date, integer, text); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE sp_uus_turniir(IN in_turniiri_nimi text, IN in_algusaeg date, IN in_paevade_arv integer, IN in_asula_nimi text)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_loppkuupaev date;
    v_asula_id integer;
    v_teade text;
BEGIN
    v_loppkuupaev := in_algusaeg + in_paevade_arv - 1;

    -- Lisab asula, kui seda pole juba olemas
    INSERT INTO asulad (nimi) VALUES (in_asula_nimi) ON CONFLICT (nimi) DO NOTHING;

    -- Hangib asula ID
    SELECT id INTO v_asula_id FROM asulad WHERE nimi = in_asula_nimi;

    -- Lisab uue turniiri
    INSERT INTO turniirid (nimi, alguskuupaev, loppkuupaev, asula)
    VALUES (in_turniiri_nimi, in_algusaeg, v_loppkuupaev, v_asula_id);

    -- Koostab teate vastavalt turniiri kestusele
    IF in_paevade_arv = 1 THEN
        v_teade := 'Lisati turniir ' || in_turniiri_nimi || ', mis toimub ' || in_algusaeg || ' asulas ' || in_asula_nimi || '.';
    ELSE
        v_teade := 'Lisati turniir ' || in_turniiri_nimi || ', mis toimub ' || in_algusaeg || ' kuni ' || v_loppkuupaev || ' asulas ' || in_asula_nimi || '.';
    END IF;

    -- Väljastab teate
    RAISE NOTICE '%', v_teade;
END;
$$;


--
-- TOC entry 274 (class 1255 OID 17241)
-- Name: sp_uus_turniir(character varying, date, integer, character varying); Type: PROCEDURE; Schema: public; Owner: -
--

CREATE PROCEDURE sp_uus_turniir(IN turniiri_nimi character varying, IN algus date, IN paevade_arv integer, IN asula_nimi character varying)
    LANGUAGE plpgsql
    AS $$
DECLARE loendur integer;
    asula_id integer;
BEGIN
    SELECT count(*) INTO loendur from Turniirid where toimumiskoht = asula_nimi;
    IF loendur = 0 THEN
        INSERT INTO asulad (nimi)
        VALUES (asula_nimi);
        END IF;
    SELECT turniirid.id INTO asula_id FROM turniirid WHERE toimumiskoht  = asula_nimi;
    INSERT INTO turniirid (nimi, alguskuupaev, loppkuupaev, toimumiskoht)
    VALUES (turniiri_nimi, algus, algus+paevade_arv-1, asula_id);
    IF paevade_arv = 1 THEN 
        RAISE NOTICE ' Lisati turniir %, mis toimub % asulas %.', turniiri_nimi, algus, asula_nimi;
    ELSE
        RAISE NOTICE 'Lisati turniir %, mis toimub % kuni % asulas %.', turniiri_nimi, algus, algus+paevade_arv-1, asula_nimi;
        END IF;
END;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 216 (class 1259 OID 17242)
-- Name: asulad; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE asulad (
    id integer NOT NULL,
    nimi character varying(100) NOT NULL
);


--
-- TOC entry 217 (class 1259 OID 17245)
-- Name: asulad_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE asulad_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4953 (class 0 OID 0)
-- Dependencies: 217
-- Name: asulad_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE asulad_id_seq OWNED BY asulad.id;


--
-- TOC entry 218 (class 1259 OID 17246)
-- Name: inimesed; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE inimesed (
    eesnimi character varying(70) NOT NULL,
    perenimi character varying(100) NOT NULL,
    sugu character(1) NOT NULL,
    synnipaev date DEFAULT CURRENT_DATE NOT NULL,
    sisestatud timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    isikukood character varying(11),
    CONSTRAINT inimesed_sugu_check CHECK ((sugu = ANY (ARRAY['m'::bpchar, 'n'::bpchar])))
);


--
-- TOC entry 219 (class 1259 OID 17252)
-- Name: isikud; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE isikud (
    id integer NOT NULL,
    eesnimi character varying(50) NOT NULL,
    perenimi character varying(50) NOT NULL,
    isikukood character varying(11),
    klubi integer,
    synniaeg date,
    sugu character(1) DEFAULT 'm'::bpchar NOT NULL,
    ranking integer
);


--
-- TOC entry 220 (class 1259 OID 17256)
-- Name: isikud_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE isikud_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4954 (class 0 OID 0)
-- Dependencies: 220
-- Name: isikud_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE isikud_id_seq OWNED BY isikud.id;


--
-- TOC entry 221 (class 1259 OID 17257)
-- Name: klubid; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE klubid (
    id integer NOT NULL,
    nimi character varying(100) NOT NULL,
    asula integer
);


--
-- TOC entry 222 (class 1259 OID 17260)
-- Name: klubid_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE klubid_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4955 (class 0 OID 0)
-- Dependencies: 222
-- Name: klubid_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE klubid_id_seq OWNED BY klubid.id;


--
-- TOC entry 223 (class 1259 OID 17261)
-- Name: partiid; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE partiid (
    turniir integer NOT NULL,
    algushetk timestamp without time zone NOT NULL,
    lopphetk timestamp without time zone,
    valge integer NOT NULL,
    must integer NOT NULL,
    valge_tulemus smallint,
    must_tulemus smallint,
    id integer NOT NULL,
    kokkuvote text
);


--
-- TOC entry 224 (class 1259 OID 17266)
-- Name: mv_partiide_arv_valgetega; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--

CREATE MATERIALIZED VIEW mv_partiide_arv_valgetega AS
 SELECT i.eesnimi,
    i.perenimi,
    COALESCE(count(p.valge), (0)::bigint) AS partiisid_valgetega
   FROM (isikud i
     LEFT JOIN partiid p ON ((i.id = p.valge)))
  GROUP BY i.eesnimi, i.perenimi
  WITH NO DATA;


--
-- TOC entry 225 (class 1259 OID 17271)
-- Name: partiid_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE partiid_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4956 (class 0 OID 0)
-- Dependencies: 225
-- Name: partiid_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE partiid_id_seq OWNED BY partiid.id;


--
-- TOC entry 226 (class 1259 OID 17272)
-- Name: riigid; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE riigid (
    id integer NOT NULL,
    nimi character varying(100) NOT NULL,
    pealinn character varying(100) NOT NULL,
    rahvaarv integer,
    pindala integer,
    skp_mld numeric(8,3)
);


--
-- TOC entry 227 (class 1259 OID 17275)
-- Name: riigid_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE riigid_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4957 (class 0 OID 0)
-- Dependencies: 227
-- Name: riigid_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE riigid_id_seq OWNED BY riigid.id;


--
-- TOC entry 228 (class 1259 OID 17276)
-- Name: turniirid; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE turniirid (
    id integer NOT NULL,
    nimi character varying(100) NOT NULL,
    alguskuupaev date NOT NULL,
    loppkuupaev date,
    asula integer NOT NULL
);


--
-- TOC entry 229 (class 1259 OID 17279)
-- Name: turniirid_asula_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE turniirid_asula_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4958 (class 0 OID 0)
-- Dependencies: 229
-- Name: turniirid_asula_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE turniirid_asula_seq OWNED BY turniirid.asula;


--
-- TOC entry 230 (class 1259 OID 17280)
-- Name: turniirid_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE turniirid_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4959 (class 0 OID 0)
-- Dependencies: 230
-- Name: turniirid_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE turniirid_id_seq OWNED BY turniirid.id;


--
-- TOC entry 231 (class 1259 OID 17281)
-- Name: v_isikudklubid; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW v_isikudklubid AS
 SELECT (((isikud.perenimi)::text || ', '::text) || (isikud.eesnimi)::text) AS isik_nimi,
    isikud.id AS isik_id,
    isikud.synniaeg,
    klubid.nimi AS klubi_nimi,
    klubid.id AS klubi_id,
    isikud.ranking
   FROM (isikud
     JOIN klubid ON ((isikud.klubi = klubid.id)));


--
-- TOC entry 232 (class 1259 OID 17285)
-- Name: v_punktid; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW v_punktid AS
 SELECT partiid.id AS partii,
    partiid.turniir,
    isikud.id AS mangija,
    'V'::text AS varv,
    ((partiid.valge_tulemus)::numeric / 2.0) AS punkt
   FROM partiid,
    isikud
  WHERE (isikud.id = partiid.valge)
UNION
 SELECT partiid.id AS partii,
    partiid.turniir,
    isikud.id AS mangija,
    'M'::text AS varv,
    ((partiid.must_tulemus)::numeric / 2.0) AS punkt
   FROM partiid,
    isikud
  WHERE (isikud.id = partiid.must);


--
-- TOC entry 233 (class 1259 OID 17290)
-- Name: v_edetabelid; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW v_edetabelid AS
 SELECT vi.isik_id AS id,
    vi.isik_nimi AS mangija,
    vi.synniaeg,
    vi.ranking,
    vi.klubi_nimi AS klubi,
    v.turniir,
    sum(v.punkt) AS punkte
   FROM v_punktid v,
    v_isikudklubid vi
  WHERE (v.mangija = vi.isik_id)
  GROUP BY vi.isik_id, vi.isik_nimi, vi.synniaeg, vi.ranking, vi.klubi_nimi, v.turniir;


--
-- TOC entry 234 (class 1259 OID 17294)
-- Name: v_keskminepartii; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW v_keskminepartii AS
 SELECT turniirid.nimi AS turniiri_nimi,
    avg(EXTRACT(minute FROM (partiid.lopphetk - partiid.algushetk))) AS keskmine_partii
   FROM (turniirid
     JOIN partiid ON ((partiid.turniir = turniirid.id)))
  GROUP BY turniirid.nimi;


--
-- TOC entry 235 (class 1259 OID 17299)
-- Name: v_klubi54; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW v_klubi54 AS
 SELECT eesnimi,
    perenimi,
    synniaeg,
    ranking,
    klubi AS klubi_id
   FROM isikud
  WHERE (klubi = 54)
  WITH CASCADED CHECK OPTION;


--
-- TOC entry 236 (class 1259 OID 17303)
-- Name: v_klubipartiikogused; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW v_klubipartiikogused AS
 SELECT klubid.nimi AS klubi_nimi,
    count(DISTINCT partiid.id) AS partiisid
   FROM ((isikud
     JOIN klubid ON ((isikud.klubi = klubid.id)))
     JOIN partiid ON (((isikud.id = partiid.valge) OR (isikud.id = partiid.must))))
  GROUP BY klubid.nimi;


--
-- TOC entry 237 (class 1259 OID 17308)
-- Name: v_maletaht; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW v_maletaht AS
 SELECT isikud.id,
    isikud.eesnimi,
    isikud.perenimi,
    isikud.isikukood,
    isikud.klubi,
    isikud.synniaeg,
    isikud.sugu,
    isikud.ranking
   FROM (isikud
     JOIN klubid ON ((isikud.klubi = klubid.id)))
  WHERE ((klubid.nimi)::text = 'Maletäht'::text);


--
-- TOC entry 238 (class 1259 OID 17312)
-- Name: v_partiidpisi; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW v_partiidpisi AS
 SELECT p.id AS partii_id,
    v.isik_nimi AS valge_mangija,
    ((p.valge_tulemus)::numeric / 2.0) AS valge_punkt,
    m.isik_nimi AS must_mangija,
    ((p.must_tulemus)::numeric / 2.0) AS must_punkt
   FROM partiid p,
    v_isikudklubid v,
    v_isikudklubid m
  WHERE ((p.valge = v.isik_id) AND (p.must = m.isik_id));


--
-- TOC entry 239 (class 1259 OID 17316)
-- Name: v_turniiripartiid; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW v_turniiripartiid AS
 SELECT t.nimi AS turniir_nimi,
    a.nimi AS toimumiskoht,
    p.id AS partii_id,
    p.algushetk AS partii_algus,
    p.lopphetk AS partii_lopp,
        CASE
            WHEN (p.valge_tulemus = 2) THEN 'valge'::text
            WHEN (p.must_tulemus = 2) THEN 'must'::text
            ELSE 'viik'::text
        END AS kes_voitis
   FROM ((partiid p
     JOIN turniirid t ON ((p.turniir = t.id)))
     JOIN asulad a ON ((t.asula = a.id)));


--
-- TOC entry 4729 (class 2604 OID 17321)
-- Name: asulad id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY asulad ALTER COLUMN id SET DEFAULT nextval('asulad_id_seq'::regclass);


--
-- TOC entry 4732 (class 2604 OID 17322)
-- Name: isikud id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY isikud ALTER COLUMN id SET DEFAULT nextval('isikud_id_seq'::regclass);


--
-- TOC entry 4734 (class 2604 OID 17323)
-- Name: klubid id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY klubid ALTER COLUMN id SET DEFAULT nextval('klubid_id_seq'::regclass);


--
-- TOC entry 4735 (class 2604 OID 17324)
-- Name: partiid id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY partiid ALTER COLUMN id SET DEFAULT nextval('partiid_id_seq'::regclass);


--
-- TOC entry 4736 (class 2604 OID 17325)
-- Name: riigid id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY riigid ALTER COLUMN id SET DEFAULT nextval('riigid_id_seq'::regclass);


--
-- TOC entry 4737 (class 2604 OID 17326)
-- Name: turniirid id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY turniirid ALTER COLUMN id SET DEFAULT nextval('turniirid_id_seq'::regclass);


--
-- TOC entry 4738 (class 2604 OID 17327)
-- Name: turniirid asula; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY turniirid ALTER COLUMN asula SET DEFAULT nextval('turniirid_asula_seq'::regclass);


--
-- TOC entry 4932 (class 0 OID 17242)
-- Dependencies: 216
-- Data for Name: asulad; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO asulad VALUES (1, 'Pärnu');
INSERT INTO asulad VALUES (2, 'Elva');
INSERT INTO asulad VALUES (3, 'Narva');
INSERT INTO asulad VALUES (4, 'Tartu');
INSERT INTO asulad VALUES (5, 'Viljandi');
INSERT INTO asulad VALUES (6, '42');
INSERT INTO asulad VALUES (7, 'Viiratsi');
INSERT INTO asulad VALUES (8, 'Kambja');
INSERT INTO asulad VALUES (9, 'Tallinn');


--
-- TOC entry 4934 (class 0 OID 17246)
-- Dependencies: 218
-- Data for Name: inimesed; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO inimesed VALUES ('Mihkel', 'Rump', 'm', '2002-05-23', '2023-05-19 19:54:36.770075', '50205230853');


--
-- TOC entry 4935 (class 0 OID 17252)
-- Dependencies: 219
-- Data for Name: isikud; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO isikud VALUES (9, 'Tarmo', 'Kooser', '37209112028', NULL, '1972-09-11', 'm', 1076);
INSERT INTO isikud VALUES (71, 'Arvo', 'Mets', '33911230101', 51, '1939-11-23', 'm', 1066);
INSERT INTO isikud VALUES (73, 'Pjotr', 'Pustota', '36602240707', 59, '1966-02-24', 'm', 1646);
INSERT INTO isikud VALUES (74, 'Kalle', 'Kivine', '36006230808', 57, '1960-06-23', 'm', 1411);
INSERT INTO isikud VALUES (147, 'Kalev', 'Jőud', '35304040404', 50, '1953-04-04', 'm', 1255);
INSERT INTO isikud VALUES (156, 'Tőnu', 'Tőrs', '34805050505', 52, '1948-05-05', 'm', 1497);
INSERT INTO isikud VALUES (78, 'Andrei', 'Sosnov', '37704220102', 59, '1977-04-22', 'm', 1813);
INSERT INTO isikud VALUES (12, 'Piia', 'Looser', '47303142014', 50, '1973-03-14', 'n', 1091);
INSERT INTO isikud VALUES (10, 'Tiina', 'Kooser', '47401010224', NULL, '1974-01-01', 'n', 1027);
INSERT INTO isikud VALUES (8, 'Taimi', 'Sabel', '47510142025', NULL, '1975-10-14', 'n', 1851);
INSERT INTO isikud VALUES (199, 'Sander', 'Saabas', '38707303030', 61, '1987-07-30', 'm', 1047);
INSERT INTO isikud VALUES (201, 'Lembit', 'Allveelaev', '36608080808', 61, '1966-08-08', 'm', 1040);
INSERT INTO isikud VALUES (13, 'Laura', 'Kask', '47303142020', NULL, '1973-03-14', 'n', 1268);
INSERT INTO isikud VALUES (6, 'Kaia', 'Maja', '47001221010', NULL, '1970-01-22', 'n', 1704);
INSERT INTO isikud VALUES (192, 'Keiu', 'Vői', '48412242424', 61, '1984-12-24', 'n', 1047);
INSERT INTO isikud VALUES (193, 'Heli', 'Jälg', '48112313131', 61, '1981-12-31', 'n', 1429);
INSERT INTO isikud VALUES (194, 'Kaja', 'Lood', '47005040405', 61, '1970-05-04', 'n', 1006);
INSERT INTO isikud VALUES (195, 'Laine', 'Hari', '46807171720', 61, '1968-07-17', 'n', 1124);
INSERT INTO isikud VALUES (196, 'Kalju', 'Saaremets', '36308171015', 61, '1963-08-17', 'm', 1205);
INSERT INTO isikud VALUES (197, 'Priit', 'Pőder', '36709291416', 61, '1967-09-29', 'm', 1666);
INSERT INTO isikud VALUES (200, 'Siim', 'Susi', '37101012048', 61, '1971-01-01', 'm', 1217);
INSERT INTO isikud VALUES (2, 'Margus', 'Muru', '37602022016', 61, '1976-02-02', 'm', 1167);
INSERT INTO isikud VALUES (90, 'Urmas', 'Ubin', '35803081803', 58, '1958-03-08', 'm', 1028);
INSERT INTO isikud VALUES (162, 'Urmas', 'Ümbrik', '37304152020', 52, '1973-04-15', 'm', 1039);
INSERT INTO isikud VALUES (198, 'Urmas', 'Uljas', '36805221413', 61, '1968-05-22', 'm', 1005);
INSERT INTO isikud VALUES (93, 'Nadja', 'Puhasmaa', '45906301219', 57, '1959-06-30', 'n', 1058);
INSERT INTO isikud VALUES (94, 'Maria', 'Lihtne', '44907172613', 54, '1949-07-17', 'n', 1075);
INSERT INTO isikud VALUES (148, 'Heli', 'Kopter', '47108271519', 50, '1971-08-27', 'n', 1654);
INSERT INTO isikud VALUES (150, 'Katrin', 'Kask', '47011182050', 50, '1970-11-18', 'n', 1298);
INSERT INTO isikud VALUES (151, 'Kati', 'Karu', '46110221681', 50, '1961-10-22', 'n', 1030);
INSERT INTO isikud VALUES (152, 'Pille', 'Porgand', '46809101030', 50, '1968-09-10', 'n', 1144);
INSERT INTO isikud VALUES (157, 'Kristi', 'Kirves', '46901173020', 52, '1969-01-17', 'n', 1050);
INSERT INTO isikud VALUES (160, 'Ulvi', 'Uus', '46802012414', 52, '1968-02-01', 'n', 1175);
INSERT INTO isikud VALUES (163, 'Tatjana', 'Umnaja', '45510092514', 53, '1955-10-09', 'n', 1045);
INSERT INTO isikud VALUES (154, 'Ingo', 'Ilus', '36712044050', 55, '1967-12-04', 'm', 1041);
INSERT INTO isikud VALUES (165, 'Aljona', 'Aljas', '46603312628', 53, '1966-03-31', 'n', 1088);
INSERT INTO isikud VALUES (171, 'Sanna', 'Sari', '47309291414', 56, '1973-09-29', 'n', 1035);
INSERT INTO isikud VALUES (173, 'Hiie', 'Hiid', '47704143256', 56, '1977-04-14', 'n', 1453);
INSERT INTO isikud VALUES (175, 'Anna', 'Raha', '46605012233', 56, '1966-05-01', 'n', 1014);
INSERT INTO isikud VALUES (186, 'Tiiu', 'Talutütar', '45406124152', 60, '1954-06-12', 'n', 1048);
INSERT INTO isikud VALUES (187, 'Ere', 'Valgus', '48108182819', 60, '1981-08-18', 'n', 1002);
INSERT INTO isikud VALUES (80, 'Henno', 'Hiis', '37907063645', 55, '1976-07-06', 'm', 1237);
INSERT INTO isikud VALUES (86, 'Toomas', 'Remmelgas', '37812082134', 54, '1978-12-08', 'm', 1010);
INSERT INTO isikud VALUES (88, 'Mihkel', 'Maakamar', '38702106253', 59, '1987-02-10', 'm', 1020);
INSERT INTO isikud VALUES (89, 'Artur', 'Muld', '36911235164', 58, '1969-11-23', 'm', 1063);
INSERT INTO isikud VALUES (92, 'Toomas', 'Umnik', '36803261144', 57, '1968-03-26', 'm', 1029);
INSERT INTO isikud VALUES (145, 'Tarmo', 'Tarm', '36710301122', 50, '1967-10-30', 'm', 1128);
INSERT INTO isikud VALUES (146, 'Peeter', 'Peet', '36502125462', 50, '1965-02-12', 'm', 1053);
INSERT INTO isikud VALUES (79, 'Helina', 'Hiis', '46909099999', 55, '1969-09-09', 'n', 1000);
INSERT INTO isikud VALUES (81, 'Irys', 'Sisalik', '46901195849', 51, '1969-01-19', 'n', 1053);
INSERT INTO isikud VALUES (82, 'Maria', 'Murakas', '46701226020', 54, '1967-01-22', 'n', 2013);
INSERT INTO isikud VALUES (83, 'Maria', 'Medvedovna', '47409193456', 58, '1974-09-19', 'n', 1492);
INSERT INTO isikud VALUES (85, 'Liis', 'Metsonen', '48006065123', 54, '1980-06-06', 'n', 1295);
INSERT INTO isikud VALUES (87, 'Anna', 'Ristik', '47606143265', 55, '1976-06-14', 'n', 1125);
INSERT INTO isikud VALUES (91, 'Jelena', 'Pirn', '46210125040', 58, '1962-10-12', 'n', 1068);
INSERT INTO isikud VALUES (72, 'Maari', 'Mustikas', '48012250202', 54, '1980-12-25', 'n', 1005);
INSERT INTO isikud VALUES (75, 'Malle', 'Maasikas', '46906220808', 57, '1969-06-22', 'n', 1645);
INSERT INTO isikud VALUES (167, 'Valve', 'Vask', '45602091010', 53, '1956-02-09', 'n', 1116);
INSERT INTO isikud VALUES (149, 'Kalju', 'Kotkas', '35306032623', 50, '1953-06-03', 'm', 1090);
INSERT INTO isikud VALUES (153, 'Ilo', 'Ilus', '37502282135', 55, '1975-02-28', 'm', 1343);
INSERT INTO isikud VALUES (155, 'Mart', 'Mari', '37602232513', 55, '1976-02-23', 'm', 1249);
INSERT INTO isikud VALUES (159, 'Tőnis', 'Tőrv', '36609112425', 52, '1966-09-11', 'm', 1289);
INSERT INTO isikud VALUES (161, 'Uljas', 'Ratsanik', '38108203514', 52, '1981-08-20', 'm', 1132);
INSERT INTO isikud VALUES (164, 'Boriss', 'Borissov', '36909211561', 53, '1969-09-21', 'm', 1039);
INSERT INTO isikud VALUES (166, 'Mihkel', 'Välk', '37009302563', 53, '1970-09-30', 'm', 1012);
INSERT INTO isikud VALUES (168, 'Peeter', 'Aljas', '36911112528', 53, '1969-11-11', 'm', 1086);
INSERT INTO isikud VALUES (169, 'Meelis', 'Meel', '36709252525', 56, '1967-09-25', 'm', 1622);
INSERT INTO isikud VALUES (170, 'Mati', 'All', '36511284135', 56, '1965-11-28', 'm', 1001);
INSERT INTO isikud VALUES (172, 'Peeter', 'Sari', '37011161616', 56, '1970-11-16', 'm', 2060);
INSERT INTO isikud VALUES (174, 'Ahto', 'Palk', '38311152463', 56, '1983-11-15', 'm', 1138);
INSERT INTO isikud VALUES (176, 'Tormi', 'Hoiatus', '38608015361', 56, '1986-08-01', 'm', 1004);
INSERT INTO isikud VALUES (177, 'Ahti', 'Mőisamees', '37701093658', 56, '1977-01-09', 'm', 1223);
INSERT INTO isikud VALUES (188, 'Toomas', 'Toom', '37501055555', 60, '1975-01-05', 'm', 1061);
INSERT INTO isikud VALUES (189, 'Kristjan', 'Kuld', '38609165632', 60, '1986-09-16', 'm', 1068);
INSERT INTO isikud VALUES (190, 'Kaarel', 'Kaaren', '36911306452', 60, '1969-11-30', 'm', 1057);
INSERT INTO isikud VALUES (191, 'Kait', 'Kalamees', '37905312634', 60, '1979-05-31', 'm', 1006);
INSERT INTO isikud VALUES (158, 'Anneli', 'Mets', '46511132627', 52, '1965-11-13', 'n', 1628);
INSERT INTO isikud VALUES (76, 'Linda', 'Sammal', '46710101010', 58, '1967-10-10', 'n', 1943);
INSERT INTO isikud VALUES (84, 'Ilona', 'Polje', '48201291516', 51, '1982-01-29', 'n', 1086);
INSERT INTO isikud VALUES (77, 'Arvo', 'Angervaks', '35911111111', 59, '1959-11-11', 'm', 1149);
INSERT INTO isikud VALUES (15, 'Joonas', 'Kask', NULL, 57, NULL, 'm', NULL);


--
-- TOC entry 4937 (class 0 OID 17257)
-- Dependencies: 221
-- Data for Name: klubid; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO klubid VALUES (59, 'Musta kivi kummardajad', 4);
INSERT INTO klubid VALUES (57, 'Vőitmatu Valge', 4);
INSERT INTO klubid VALUES (55, 'Ruudu Liine', 4);
INSERT INTO klubid VALUES (51, 'Laudnikud', 4);
INSERT INTO klubid VALUES (54, 'Ajurebend', 4);
INSERT INTO klubid VALUES (58, 'Valge Mask', 4);
INSERT INTO klubid VALUES (50, 'Raudne Ratsu', 9);
INSERT INTO klubid VALUES (52, 'Pärnu Parimad', 1);
INSERT INTO klubid VALUES (53, 'Vabaettur', 3);
INSERT INTO klubid VALUES (56, 'Maletäht', 9);
INSERT INTO klubid VALUES (60, 'Chess', 5);
INSERT INTO klubid VALUES (61, 'Areng', 9);
INSERT INTO klubid VALUES (1, 'Tallinna ratsud', 9);
INSERT INTO klubid VALUES (3, 'Odamehed', 4);


--
-- TOC entry 4939 (class 0 OID 17261)
-- Dependencies: 223
-- Data for Name: partiid; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO partiid VALUES (43, '2006-06-04 08:01:00', '2006-06-04 08:33:22', 150, 75, 2, 0, 1, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 13:01:00', '2006-06-04 13:29:01', 152, 91, 1, 1, 2, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 11:01:00', '2005-03-04 11:27:01', 87, 93, 2, 0, 3, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 13:01:00', '2006-06-04 13:11:24', 193, 148, 1, 1, 4, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 16:01:00', '2005-03-04 16:22:52', 71, 73, 0, 2, 5, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 13:09:00', '2005-01-12 13:32:17', 93, 75, 0, 2, 6, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 10:02:00', '2007-09-01 10:22:44', 195, 152, 1, 1, 7, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 09:02:00', '2007-09-01 09:26:18', 176, 82, 2, 0, 8, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 16:01:00', '2007-09-01 16:17:08', 172, 168, 2, 0, 9, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 10:01:00', '2007-09-01 10:41:40', 175, 165, 2, 0, 10, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 10:01:00', '2010-10-14 10:27:26', 91, 81, 0, 2, 11, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 12:01:00', '2010-10-14 12:21:52', 80, 73, 1, 1, 12, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 10:02:00', '2005-03-04 10:29:06', 85, 80, 2, 0, 13, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 16:02:00', '2005-01-12 16:24:16', 93, 74, 0, 2, 14, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 14:01:00', '2007-09-01 14:17:56', 153, 82, 0, 2, 15, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 13:01:00', '2006-06-04 13:34:30', 161, 77, 1, 1, 16, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 16:03:00', '2005-03-04 16:39:04', 79, 90, 1, 1, 17, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 12:01:00', '2006-06-04 12:13:02', 171, 166, 0, 2, 18, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 13:01:00', '2006-06-04 13:28:44', 192, 187, 1, 1, 19, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 17:02:00', '2006-06-04 17:41:18', 191, 165, 2, 0, 20, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 16:02:00', '2006-06-04 16:32:01', 199, 177, 1, 1, 21, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 11:02:00', '2010-10-14 11:22:07', 90, 81, 1, 1, 22, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 15:01:00', '2007-09-01 15:28:50', 171, 161, 1, 1, 23, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 16:02:00', '2005-01-12 16:24:07', 92, 75, 1, 1, 24, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 10:01:00', '2005-03-04 10:30:50', 76, 82, 1, 1, 25, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 08:01:00', '2006-06-04 08:28:19', 148, 145, 1, 1, 26, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 15:01:00', '2005-03-04 15:22:43', 81, 85, 2, 0, 28, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 09:02:00', '2006-06-04 09:36:04', 190, 162, 1, 1, 29, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 11:01:00', '2006-06-04 11:22:59', 147, 86, 2, 0, 30, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 11:01:00', '2006-06-04 11:21:20', 191, 167, 2, 0, 31, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 09:02:00', '2005-03-04 09:23:07', 88, 76, 2, 0, 32, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 10:02:00', '2006-06-04 10:14:53', 152, 83, 1, 1, 33, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 11:03:00', '2010-10-14 11:37:51', 94, 88, 1, 1, 34, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 17:03:00', '2006-06-04 17:40:26', 79, 78, 0, 2, 36, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 10:05:00', '2010-10-14 10:36:14', 90, 88, 1, 1, 37, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 12:01:00', '2007-09-01 12:33:03', 189, 188, 2, 0, 38, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 16:02:00', '2005-03-04 16:35:18', 88, 87, 2, 0, 39, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 12:01:00', '2005-03-04 12:25:51', 87, 82, 0, 2, 42, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 14:01:00', '2007-09-01 14:35:05', 172, 165, 2, 0, 45, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 14:01:00', '2010-10-14 14:23:45', 94, 81, 1, 1, 46, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 16:01:00', '2007-09-01 16:28:23', 201, 73, 0, 2, 48, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 12:01:00', '2007-09-01 12:28:15', 170, 87, 2, 0, 49, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 09:03:00', '2005-03-04 09:33:11', 82, 92, 1, 1, 50, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 15:01:00', '2007-09-01 15:18:58', 198, 82, 0, 2, 51, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 14:01:00', '2006-06-04 14:33:26', 192, 161, 0, 2, 52, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 16:02:00', '2005-01-12 16:14:40', 77, 73, 0, 2, 53, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 12:03:00', '2005-03-04 12:19:28', 89, 75, 1, 1, 54, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 08:04:00', '2010-10-14 08:28:49', 89, 82, 2, 0, 55, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 16:02:00', '2006-06-04 16:26:21', 197, 159, 2, 0, 56, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 10:03:00', '2005-03-04 10:31:36', 81, 77, 0, 2, 57, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 11:08:00', '2005-01-12 11:35:48', 78, 92, 2, 0, 58, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 13:04:00', '2005-03-04 13:14:50', 87, 81, 0, 2, 59, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 09:01:00', '2006-06-04 09:22:46', 151, 87, 0, 2, 60, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:19:22', 171, 83, 0, 2, 62, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 09:10:00', '2010-10-14 09:45:48', 94, 84, 1, 1, 63, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 16:01:00', '2006-06-04 16:39:54', 201, 147, 0, 2, 64, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 17:01:00', '2006-06-04 17:25:42', 156, 86, 2, 0, 66, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 13:01:00', '2007-09-01 13:31:37', 81, 74, 0, 2, 67, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 17:01:00', '2010-10-14 17:16:56', 83, 82, 2, 0, 69, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 11:02:00', '2007-09-01 11:28:41', 160, 157, 2, 0, 70, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 14:06:00', '2005-01-12 14:24:26', 73, 74, 2, 0, 71, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 17:02:00', '2006-06-04 17:18:34', 175, 152, 1, 1, 72, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:15:54', 187, 84, 1, 1, 73, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 14:01:00', '2010-10-14 14:22:13', 87, 84, 1, 1, 74, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 11:03:00', '2005-03-04 11:24:35', 92, 76, 1, 1, 75, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 11:03:00', '2005-01-12 11:31:54', 75, 80, 2, 0, 76, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 15:01:00', '2006-06-04 15:19:57', 168, 85, 2, 0, 78, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 16:02:00', '2007-09-01 16:37:18', 188, 146, 0, 2, 79, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 09:01:00', '2005-03-04 09:19:08', 91, 71, 2, 0, 80, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 12:03:00', '2006-06-04 12:30:47', 173, 77, 1, 1, 81, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 15:02:00', '2005-03-04 15:26:39', 73, 76, 1, 1, 82, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 14:01:00', '2006-06-04 14:20:49', 191, 85, 1, 1, 83, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 09:01:00', '2006-06-04 09:19:52', 157, 85, 0, 2, 84, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 12:01:00', '2006-06-04 12:31:28', 156, 72, 2, 0, 86, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 11:02:00', '2006-06-04 11:25:11', 199, 195, 2, 0, 87, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 10:01:00', '2006-06-04 10:24:47', 190, 145, 1, 1, 88, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 08:04:00', '2007-09-01 08:22:49', 147, 83, 0, 2, 89, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 13:02:00', '2007-09-01 13:36:46', 198, 188, 2, 0, 90, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 15:01:00', '2006-06-04 15:16:17', 167, 166, 2, 0, 91, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 12:01:00', '2007-09-01 12:20:30', 201, 198, 2, 0, 92, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 16:01:00', '2007-09-01 16:31:21', 149, 93, 2, 0, 93, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 09:01:00', '2005-03-04 09:15:26', 89, 73, 1, 1, 95, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 10:02:00', '2005-03-04 10:26:31', 75, 84, 2, 0, 96, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 10:05:00', '2005-01-12 10:29:15', 93, 87, 1, 1, 97, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 12:01:00', '2006-06-04 12:31:07', 188, 78, 1, 1, 98, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:30:59', 167, 156, 0, 2, 99, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:28:37', 175, 162, 2, 0, 100, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 16:02:00', '2006-06-04 16:21:20', 192, 155, 0, 2, 101, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 12:01:00', '2005-03-04 12:19:44', 73, 81, 1, 1, 102, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 16:04:00', '2010-10-14 16:23:00', 90, 72, 0, 2, 103, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 12:01:00', '2006-06-04 12:25:08', 172, 160, 1, 1, 104, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 12:02:00', '2005-01-12 12:25:05', 92, 87, 2, 0, 105, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 17:01:00', '2007-09-01 17:31:29', 146, 75, 2, 0, 107, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 08:01:00', '2007-09-01 08:18:13', 191, 167, 0, 2, 108, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 17:01:00', '2005-03-04 17:21:52', 82, 72, 2, 0, 109, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 10:01:00', '2007-09-01 10:33:30', 172, 79, 1, 1, 110, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 08:02:00', '2005-01-12 08:19:28', 73, 92, 1, 1, 111, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 13:01:00', '2007-09-01 13:30:35', 200, 146, 0, 2, 112, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 08:03:00', '2006-06-04 08:35:03', 168, 91, 2, 0, 113, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 10:02:00', '2006-06-04 10:17:30', 175, 148, 1, 1, 114, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 12:03:00', '2007-09-01 12:31:06', 167, 163, 0, 2, 116, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 15:01:00', '2005-03-04 15:25:22', 83, 80, 1, 1, 117, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 16:01:00', '2005-03-04 16:30:37', 89, 84, 1, 1, 118, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 13:07:00', '2005-01-12 13:32:46', 78, 74, 0, 2, 119, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:23:23', 165, 92, 0, 2, 120, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 13:01:00', '2010-10-14 13:27:29', 91, 84, 0, 2, 121, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 10:01:00', '2006-06-04 10:20:52', 193, 176, 1, 1, 122, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 17:01:00', '2007-09-01 17:22:34', 86, 74, 2, 0, 124, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 09:03:00', '2005-01-12 09:30:53', 75, 79, 2, 0, 125, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 15:04:00', '2010-10-14 15:26:44', 89, 77, 2, 0, 126, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 12:10:00', '2010-10-14 12:30:06', 87, 77, 1, 1, 127, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 14:01:00', '2005-03-04 14:29:17', 72, 76, 2, 0, 128, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 09:01:00', '2007-09-01 09:21:14', 166, 72, 1, 1, 129, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 10:01:00', '2007-09-01 10:30:44', 87, 72, 0, 2, 130, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 14:03:00', '2005-03-04 14:25:29', 75, 82, 2, 0, 131, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 13:01:00', '2010-10-14 13:21:17', 73, 72, 1, 1, 133, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 10:01:00', '2007-09-01 10:25:44', 200, 155, 0, 2, 135, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 16:02:00', '2005-03-04 16:33:14', 91, 77, 2, 0, 136, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 16:01:00', '2007-09-01 16:25:27', 164, 158, 0, 2, 137, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 11:01:00', '2005-03-04 11:25:14', 85, 89, 1, 1, 138, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 08:01:00', '2006-06-04 08:29:10', 196, 160, 1, 1, 139, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 08:02:00', '2007-09-01 08:28:03', 195, 172, 1, 1, 140, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 09:01:00', '2006-06-04 09:35:36', 172, 78, 0, 2, 141, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 17:01:00', '2007-09-01 17:27:31', 167, 77, 2, 0, 142, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 16:02:00', '2007-09-01 16:25:41', 186, 82, 0, 2, 143, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 09:01:00', '2006-06-04 09:23:35', 191, 71, 1, 1, 144, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:20:20', 159, 148, 1, 1, 145, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 12:02:00', '2006-06-04 12:21:05', 153, 84, 2, 0, 146, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 13:01:00', '2007-09-01 13:23:54', 197, 90, 2, 0, 147, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 11:01:00', '2006-06-04 11:21:29', 172, 71, 0, 2, 148, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 12:02:00', '2006-06-04 12:31:59', 157, 92, 0, 2, 150, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 15:01:00', '2007-09-01 15:18:10', 194, 80, 2, 0, 151, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 17:02:00', '2006-06-04 17:24:39', 157, 72, 0, 2, 152, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 12:03:00', '2005-03-04 12:26:21', 83, 79, 1, 1, 153, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 15:01:00', '2006-06-04 15:32:38', 197, 176, 2, 0, 154, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 16:01:00', '2007-09-01 16:26:22', 190, 77, 1, 1, 155, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 17:01:00', '2007-09-01 17:24:23', 173, 171, 0, 2, 156, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 16:02:00', '2005-03-04 16:35:18', 80, 82, 0, 2, 157, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 09:01:00', '2007-09-01 09:19:09', 175, 84, 1, 1, 158, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 11:01:00', '2006-06-04 11:32:10', 165, 72, 2, 0, 159, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 09:01:00', '2005-03-04 09:33:28', 78, 75, 0, 2, 160, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 09:01:00', '2007-09-01 09:22:25', 159, 153, 1, 1, 162, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 17:05:00', '2005-03-04 17:27:42', 92, 83, 1, 1, 163, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 12:01:00', '2006-06-04 12:14:51', 152, 81, 1, 1, 164, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 10:01:00', '2005-03-04 10:14:20', 91, 83, 2, 0, 165, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 12:02:00', '2007-09-01 12:20:01', 200, 173, 0, 2, 166, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 08:04:00', '2005-01-12 08:35:35', 77, 87, 2, 0, 167, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 16:02:00', '2006-06-04 16:16:48', 186, 81, 2, 0, 168, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 16:01:00', '2006-06-04 16:26:22', 200, 76, 1, 1, 169, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 09:04:00', '2010-10-14 09:23:35', 85, 83, 0, 2, 170, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 10:01:00', '2006-06-04 10:32:00', 171, 164, 0, 2, 171, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 17:01:00', '2006-06-04 17:37:03', 173, 94, 1, 1, 172, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:25:33', 150, 93, 0, 2, 173, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 16:01:00', '2006-06-04 16:29:59', 93, 72, 2, 0, 174, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 12:04:00', '2005-01-12 12:22:23', 73, 79, 0, 2, 175, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 12:01:00', '2006-06-04 12:25:45', 190, 93, 0, 2, 176, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 08:02:00', '2006-06-04 08:39:56', 198, 191, 1, 1, 177, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 08:03:00', '2010-10-14 08:22:14', 87, 85, 1, 1, 178, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 16:05:00', '2005-01-12 16:31:44', 78, 80, 1, 1, 179, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 16:02:00', '2010-10-14 16:26:46', 89, 79, 2, 0, 180, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 13:03:00', '2006-06-04 13:29:28', 89, 86, 1, 1, 181, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 10:01:00', '2005-03-04 10:17:15', 72, 74, 2, 0, 182, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 10:01:00', '2006-06-04 10:21:23', 74, 72, 1, 1, 183, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 13:01:00', '2006-06-04 13:29:58', 200, 162, 2, 0, 184, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 08:01:00', '2005-03-04 08:14:49', 87, 79, 0, 2, 185, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 13:04:00', '2005-01-12 13:29:53', 88, 80, 0, 2, 186, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 17:01:00', '2007-09-01 17:15:22', 166, 80, 1, 1, 187, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 12:01:00', '2007-09-01 12:28:28', 80, 76, 2, 0, 188, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 12:01:00', '2006-06-04 12:31:41', 161, 88, 1, 1, 189, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 12:09:00', '2005-01-12 12:41:36', 77, 74, 1, 1, 190, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 15:01:00', '2005-03-04 15:19:05', 90, 91, 2, 0, 191, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 16:01:00', '2007-09-01 16:27:29', 91, 72, 1, 1, 192, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 15:01:00', '2007-09-01 15:39:55', 169, 79, 1, 1, 193, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 13:05:00', '2010-10-14 13:33:30', 88, 82, 0, 2, 194, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 09:01:00', '2005-01-12 09:26:50', 78, 77, 2, 0, 195, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 14:03:00', '2005-03-04 14:17:21', 91, 84, 2, 0, 196, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 14:01:00', '2006-06-04 14:26:53', 186, 87, 2, 0, 197, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 09:01:00', '2010-10-14 09:21:04', 90, 78, 1, 1, 198, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 12:01:00', '2007-09-01 12:25:37', 155, 150, 0, 2, 200, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 12:02:00', '2007-09-01 12:31:31', 169, 165, 2, 0, 201, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 13:02:00', '2006-06-04 13:30:53', 172, 145, 1, 1, 202, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 10:01:00', '2007-09-01 10:31:05', 94, 74, 1, 1, 203, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 14:02:00', '2006-06-04 14:38:17', 94, 78, 0, 2, 204, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 17:01:00', '2005-03-04 17:27:37', 81, 78, 0, 2, 205, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 12:01:00', '2007-09-01 12:41:24', 190, 79, 1, 1, 208, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 12:01:00', '2007-09-01 12:17:57', 186, 148, 1, 1, 209, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 13:01:00', '2006-06-04 13:34:46', 186, 79, 2, 0, 210, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 15:01:00', '2005-03-04 15:27:03', 77, 72, 1, 1, 211, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 13:01:00', '2005-03-04 13:25:01', 76, 93, 1, 1, 212, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 08:01:00', '2006-06-04 08:30:11', 174, 90, 2, 0, 213, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 13:02:00', '2006-06-04 13:18:42', 169, 168, 1, 1, 214, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 08:01:00', '2005-03-04 08:17:12', 71, 93, 0, 2, 215, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 09:03:00', '2007-09-01 09:32:16', 195, 74, 0, 2, 216, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 12:02:00', '2006-06-04 12:26:05', 194, 186, 0, 2, 217, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 17:01:00', '2010-10-14 17:25:52', 89, 85, 2, 0, 218, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 09:01:00', '2006-06-04 09:28:56', 82, 74, 0, 2, 222, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 15:02:00', '2007-09-01 15:25:08', 160, 74, 1, 1, 223, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 14:01:00', '2007-09-01 14:29:53', 156, 155, 1, 1, 224, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 09:04:00', '2010-10-14 09:33:34', 88, 86, 0, 2, 225, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 09:01:00', '2007-09-01 09:20:47', 161, 152, 0, 2, 226, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 11:04:00', '2010-10-14 11:17:54', 83, 80, 2, 0, 227, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 11:01:00', '2005-03-04 11:34:58', 82, 78, 2, 0, 228, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 14:01:00', '2006-06-04 14:28:13', 160, 72, 0, 2, 229, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 08:01:00', '2010-10-14 08:33:12', 90, 86, 1, 1, 230, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 17:01:00', '2006-06-04 17:21:44', 162, 80, 2, 0, 231, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 09:06:00', '2010-10-14 09:16:42', 89, 73, 1, 1, 233, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 08:01:00', '2005-03-04 08:20:45', 73, 82, 1, 1, 234, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 15:02:00', '2005-03-04 15:25:22', 86, 74, 1, 1, 235, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 11:01:00', '2006-06-04 11:16:37', 85, 81, 0, 2, 236, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 16:03:00', '2006-06-04 16:23:12', 175, 80, 0, 2, 237, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 13:01:00', '2010-10-14 13:19:02', 90, 76, 1, 1, 238, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 09:03:00', '2005-01-12 09:21:57', 88, 92, 1, 1, 239, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 15:03:00', '2010-10-14 15:29:37', 79, 78, 0, 2, 240, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 10:02:00', '2010-10-14 10:39:29', 85, 77, 0, 2, 241, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 08:02:00', '2005-03-04 08:25:43', 92, 84, 1, 1, 242, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 10:01:00', '2007-09-01 10:21:28', 190, 83, 1, 1, 243, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 16:01:00', '2010-10-14 16:28:27', 91, 82, 0, 2, 245, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 15:07:00', '2010-10-14 15:30:53', 86, 83, 2, 0, 246, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 14:04:00', '2005-03-04 14:18:37', 78, 85, 2, 0, 247, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 16:04:00', '2007-09-01 16:30:28', 167, 74, 2, 0, 248, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 17:02:00', '2005-01-12 17:14:43', 78, 79, 1, 1, 249, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 14:01:00', '2007-09-01 14:19:56', 169, 80, 1, 1, 250, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 17:03:00', '2005-03-04 17:19:04', 74, 79, 0, 2, 251, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 17:01:00', '2007-09-01 17:25:54', 169, 78, 1, 1, 252, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 09:01:00', '2006-06-04 09:28:16', 160, 75, 0, 2, 253, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 17:02:00', '2007-09-01 17:35:01', 192, 94, 0, 2, 254, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 12:01:00', '2007-09-01 12:32:52', 193, 73, 1, 1, 255, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 12:02:00', '2010-10-14 12:25:51', 89, 84, 2, 0, 257, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 10:03:00', '2006-06-04 10:37:49', 165, 161, 0, 2, 258, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 14:02:00', '2005-03-04 14:30:33', 89, 80, 1, 1, 259, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 17:02:00', '2006-06-04 17:25:11', 197, 149, 2, 0, 260, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 09:01:00', '2006-06-04 09:23:47', 165, 159, 0, 2, 262, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 14:01:00', '2007-09-01 14:23:08', 84, 71, 0, 2, 263, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 09:01:00', '2006-06-04 09:28:54', 188, 175, 2, 0, 264, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 12:01:00', '2007-09-01 12:27:05', 162, 159, 1, 1, 265, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 09:01:00', '2007-09-01 09:32:31', 191, 75, 2, 0, 266, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 17:01:00', '2010-10-14 17:40:04', 87, 73, 0, 2, 267, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 16:02:00', '2005-03-04 16:12:26', 72, 85, 2, 0, 269, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 10:01:00', '2006-06-04 10:28:51', 147, 78, 2, 0, 270, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 13:01:00', '2005-03-04 13:22:58', 71, 79, 0, 2, 271, NULL);
INSERT INTO partiid VALUES (42, '2005-03-04 10:01:00', '2005-03-04 10:30:31', 89, 78, 1, 1, 274, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 14:01:00', '2006-06-04 14:28:01', 197, 89, 1, 1, 275, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 14:02:00', '2007-09-01 14:23:37', 198, 171, 1, 1, 276, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 13:03:00', '2010-10-14 13:21:13', 78, 71, 0, 2, 277, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 12:02:00', '2006-06-04 12:25:21', 149, 85, 1, 1, 278, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:23:30', 192, 173, 1, 1, 281, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 14:05:00', '2005-01-12 14:31:47', 78, 75, 0, 2, 282, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 16:01:00', '2007-09-01 16:33:38', 157, 78, 1, 1, 283, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 08:01:00', '2006-06-04 08:27:38', 170, 153, 2, 0, 285, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:18:16', 191, 170, 0, 2, 286, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 10:01:00', '2007-09-01 10:22:31', 86, 71, 2, 0, 287, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 10:01:00', '2007-09-01 10:25:09', 201, 169, 1, 1, 288, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 14:01:00', '2007-09-01 14:21:26', 193, 157, 2, 0, 289, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 11:01:00', '2006-06-04 11:27:17', 168, 155, 0, 2, 290, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 08:01:00', '2006-06-04 08:21:21', 192, 156, 0, 2, 291, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 17:01:00', '2006-06-04 17:21:39', 174, 168, 0, 2, 292, NULL);
INSERT INTO partiid VALUES (43, '2006-06-04 09:01:00', '2006-06-04 09:38:35', 194, 147, 2, 0, 293, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 11:01:00', '2007-09-01 11:23:51', 82, 77, 1, 1, 294, NULL);
INSERT INTO partiid VALUES (47, '2010-10-14 11:02:00', '2010-10-14 11:26:28', 82, 71, 2, 0, 296, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 08:01:00', '2007-09-01 08:32:47', 162, 90, 0, 2, 297, NULL);
INSERT INTO partiid VALUES (44, '2007-09-01 17:01:00', '2007-09-01 17:22:34', 198, 168, 1, 1, 298, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 08:05:00', NULL, 201, 189, 1, 1, 300, NULL);
INSERT INTO partiid VALUES (41, '2005-01-12 08:05:00', NULL, 201, 189, 1, 1, 302, NULL);


--
-- TOC entry 4942 (class 0 OID 17272)
-- Dependencies: 226
-- Data for Name: riigid; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO riigid VALUES (12, 'Albania', 'Tirana', 2876591, 28748, 15.290);
INSERT INTO riigid VALUES (23, 'Armenia', 'Yerevan', 2924816, 29743, 11.550);
INSERT INTO riigid VALUES (6, 'Azerbaijan', 'Baku', 9911646, 86600, 39.210);
INSERT INTO riigid VALUES (32, 'Australia', 'Canberra', 25023700, 7692024, 1500.000);
INSERT INTO riigid VALUES (4, 'Austria', 'Vienna', 8823054, 83897, 477.670);
INSERT INTO riigid VALUES (16, 'Belarus', 'Minsk', 9494800, 207595, 59.000);
INSERT INTO riigid VALUES (13, 'Belgium', 'Brussels', 11358357, 30528, 562.230);
INSERT INTO riigid VALUES (18, 'Bulgaria', 'Sofia', 7050034, 110993, 55.950);
INSERT INTO riigid VALUES (20, 'Croatia', 'Zagreb', 4154200, 56594, 61.060);
INSERT INTO riigid VALUES (14, 'Czech Republic', 'Prague', 10610947, 78866, 238.000);
INSERT INTO riigid VALUES (26, 'Cyprus', 'Nicosia  ', 1170125, 9251, 19.810);
INSERT INTO riigid VALUES (5, 'Denmark', 'Copenhagen', 5785864, 42933, 340.980);
INSERT INTO riigid VALUES (17, 'Estonia', 'Tallinn', 1319133, 45227, 30.820);
INSERT INTO riigid VALUES (22, 'Finland', 'Helsinki', 5509717, 338424, 289.560);
INSERT INTO riigid VALUES (42, 'France', 'Paris', 67186638, 640679, 2583.000);
INSERT INTO riigid VALUES (33, 'Georgia', 'Tbilisi', 3718200, 69700, 15.020);
INSERT INTO riigid VALUES (7, 'Germany', 'Berlin', 82800000, 357386, 3685.000);
INSERT INTO riigid VALUES (21, 'Greece', 'Athens', 10768477, 131957, 221.570);
INSERT INTO riigid VALUES (36, 'Hungary', 'Budapest', 9797561, 93030, 163.540);
INSERT INTO riigid VALUES (11, 'Iceland', 'Reykjavík', 350710, 102775, 25.000);
INSERT INTO riigid VALUES (25, 'Ireland', 'Dublin', 4792500, 70273, 385.000);
INSERT INTO riigid VALUES (10, 'Israel', 'Jerusalem', 8896680, 20770, 373.750);
INSERT INTO riigid VALUES (43, 'Italy', 'Rome', 60483973, 301340, 2181.000);
INSERT INTO riigid VALUES (37, 'Latvia', 'Riga', 1925700, 64589, 30.180);
INSERT INTO riigid VALUES (15, 'Lithuania', 'Vilnius', 2800667, 65300, 54.350);
INSERT INTO riigid VALUES (19, 'North Macedonia', 'Skopje', 2103721, 25713, 12.290);
INSERT INTO riigid VALUES (35, 'Malta', 'Valletta', 475700, 316, 13.330);
INSERT INTO riigid VALUES (30, 'Moldova', 'Chișinău', 2998235, 33846, 9.200);
INSERT INTO riigid VALUES (38, 'Montenegro', 'Podgorica', 642550, 13812, 4.020);
INSERT INTO riigid VALUES (31, 'Netherlands', 'Amsterdam', 17215830, 41543, 945.330);
INSERT INTO riigid VALUES (8, 'Norway', 'Oslo', 5295719, 385203, 443.000);
INSERT INTO riigid VALUES (34, 'Poland', 'Warsaw', 38433600, 312696, 614.190);
INSERT INTO riigid VALUES (1, 'Portugal', 'Lisbon', 10291027, 92212, 279.770);
INSERT INTO riigid VALUES (27, 'Romania', 'Bucharest', 19638000, 238397, 204.940);
INSERT INTO riigid VALUES (9, 'Russia', 'Moscow', 144526636, 17098246, 1719.000);
INSERT INTO riigid VALUES (29, 'San Marino', 'San Marino', 33537, 61, 1.060);
INSERT INTO riigid VALUES (28, 'Serbia', 'Belgrade', 7040272, 88361, 42.380);
INSERT INTO riigid VALUES (39, 'Slovenia', 'Ljubljana', 2066880, 20273, 56.930);
INSERT INTO riigid VALUES (40, 'Spain', 'Madrid', 46700000, 505990, 1506.000);
INSERT INTO riigid VALUES (3, 'Sweden', 'Stockholm', 10161797, 450295, 601.000);
INSERT INTO riigid VALUES (24, 'Switzerland', 'Bern', 8401120, 41285, 681.000);
INSERT INTO riigid VALUES (2, 'Ukraine', 'Kiev', 42418235, 603628, 104.000);
INSERT INTO riigid VALUES (41, 'United Kingdom', 'London', 66040229, 242495, 2624.000);
INSERT INTO riigid VALUES (44, 'Brazil', 'Brasília', 209129000, 8515767, 2139.000);
INSERT INTO riigid VALUES (45, 'Bosnia and Herzegovina', 'Sarajevo', 3856181, 51129, 18.060);
INSERT INTO riigid VALUES (46, 'Turkey', 'Ankara', 80810525, 783356, 909.000);
INSERT INTO riigid VALUES (47, 'Canada', 'Ottawa', 37067011, 9984670, 1798.000);
INSERT INTO riigid VALUES (48, 'South Korea', 'Seoul', 51446201, 100210, 1693.000);
INSERT INTO riigid VALUES (49, 'Kyrgyzstan', 'Bishkek', 6019480, 199951, 7.060);
INSERT INTO riigid VALUES (50, 'Turkmenistan', 'Ashgabat', 5662544, 491210, 42.360);
INSERT INTO riigid VALUES (51, 'Malaysia', 'Kuala Lumpur', 32049700, 330803, 364.920);
INSERT INTO riigid VALUES (52, 'United States of America', 'Washington', 325719178, 9833520, 19390.000);
INSERT INTO riigid VALUES (53, 'Slovakia', 'Bratislava', 5435343, 49035, 111.000);
INSERT INTO riigid VALUES (54, 'Kosovo', 'Pristina', 1920079, 10908, 7.070);
INSERT INTO riigid VALUES (55, 'Guatemala', 'Guatemala City', 17263239, 108889, 82.360);
INSERT INTO riigid VALUES (56, 'Iran', 'Tehran', 81672300, 1648195, 438.000);
INSERT INTO riigid VALUES (57, 'Indonesia', 'Jakarta', 261115456, 1904569, 1074.000);
INSERT INTO riigid VALUES (58, 'Kenya', 'Nairobi', 49125325, 580367, 85.980);
INSERT INTO riigid VALUES (59, 'Andorra', 'Andorra la Vella', 77281, 468, 3.250);
INSERT INTO riigid VALUES (60, 'India', 'New Delhi', 1324171354, 3287263, 2848.000);
INSERT INTO riigid VALUES (61, 'Tajikistan', 'Dushanbe', 9537645, 143100, 7.350);
INSERT INTO riigid VALUES (62, 'Suriname', 'Paramaribo', 575990, 163821, 4.110);
INSERT INTO riigid VALUES (63, 'Congo', 'Kinshasa', 105044646, 2345409, 46.120);
INSERT INTO riigid VALUES (64, 'Cuba', 'Havana', 11181595, 109884, 107.350);


--
-- TOC entry 4944 (class 0 OID 17276)
-- Dependencies: 228
-- Data for Name: turniirid; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO turniirid VALUES (47, 'Plekkkarikas 2010', '2010-10-14', '2010-10-14', 2);
INSERT INTO turniirid VALUES (42, 'Tartu lahtised meistrivőistlused 2005', '2005-03-04', '2005-03-17', 4);
INSERT INTO turniirid VALUES (1, 'Tartu Meister', '2023-02-02', '2023-02-04', 6);
INSERT INTO turniirid VALUES (43, 'Viljandi lahtised meistrivőistlused 2006', '2006-06-04', '2006-06-04', 7);
INSERT INTO turniirid VALUES (41, 'Kolme klubi kohtumine', '2005-01-12', '2005-01-12', 8);
INSERT INTO turniirid VALUES (44, 'Eesti meistrivőistlused 2007', '2007-09-01', '2007-09-01', 9);
INSERT INTO turniirid VALUES (9, 'Tartu Meister 2023', '2023-02-02', '2023-02-04', 4);


--
-- TOC entry 4960 (class 0 OID 0)
-- Dependencies: 217
-- Name: asulad_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('asulad_id_seq', 11, true);


--
-- TOC entry 4961 (class 0 OID 0)
-- Dependencies: 220
-- Name: isikud_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('isikud_id_seq', 17, true);


--
-- TOC entry 4962 (class 0 OID 0)
-- Dependencies: 222
-- Name: klubid_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('klubid_id_seq', 7, true);


--
-- TOC entry 4963 (class 0 OID 0)
-- Dependencies: 225
-- Name: partiid_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('partiid_id_seq', 303, true);


--
-- TOC entry 4964 (class 0 OID 0)
-- Dependencies: 227
-- Name: riigid_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('riigid_id_seq', 8, true);


--
-- TOC entry 4965 (class 0 OID 0)
-- Dependencies: 229
-- Name: turniirid_asula_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('turniirid_asula_seq', 6, true);


--
-- TOC entry 4966 (class 0 OID 0)
-- Dependencies: 230
-- Name: turniirid_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('turniirid_id_seq', 9, true);


--
-- TOC entry 4741 (class 2606 OID 17329)
-- Name: asulad asulad_nimi_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY asulad
    ADD CONSTRAINT asulad_nimi_key UNIQUE (nimi);


--
-- TOC entry 4743 (class 2606 OID 17331)
-- Name: asulad asulad_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY asulad
    ADD CONSTRAINT asulad_pkey PRIMARY KEY (id);


--
-- TOC entry 4745 (class 2606 OID 17333)
-- Name: inimesed inimesed_isikukood_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY inimesed
    ADD CONSTRAINT inimesed_isikukood_key UNIQUE (isikukood);


--
-- TOC entry 4747 (class 2606 OID 17335)
-- Name: inimesed inimesed_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY inimesed
    ADD CONSTRAINT inimesed_pkey PRIMARY KEY (eesnimi, perenimi, synnipaev);


--
-- TOC entry 4749 (class 2606 OID 17337)
-- Name: isikud isikud_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY isikud
    ADD CONSTRAINT isikud_pk PRIMARY KEY (id);


--
-- TOC entry 4754 (class 2606 OID 17339)
-- Name: klubid klubid_nimi_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY klubid
    ADD CONSTRAINT klubid_nimi_key UNIQUE (nimi);


--
-- TOC entry 4756 (class 2606 OID 17341)
-- Name: klubid klubid_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY klubid
    ADD CONSTRAINT klubid_pk PRIMARY KEY (id);


--
-- TOC entry 4752 (class 2606 OID 17343)
-- Name: isikud nimi_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY isikud
    ADD CONSTRAINT nimi_unique UNIQUE (eesnimi, perenimi);


--
-- TOC entry 4758 (class 2606 OID 17345)
-- Name: partiid partiid_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY partiid
    ADD CONSTRAINT partiid_pk PRIMARY KEY (id);


--
-- TOC entry 4763 (class 2606 OID 17347)
-- Name: riigid riigid_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY riigid
    ADD CONSTRAINT riigid_pkey PRIMARY KEY (id);


--
-- TOC entry 4765 (class 2606 OID 17349)
-- Name: turniirid turniirid_nimi_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY turniirid
    ADD CONSTRAINT turniirid_nimi_key UNIQUE (nimi);


--
-- TOC entry 4767 (class 2606 OID 17351)
-- Name: turniirid turniirid_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY turniirid
    ADD CONSTRAINT turniirid_pk PRIMARY KEY (id);


--
-- TOC entry 4750 (class 1259 OID 17352)
-- Name: ix_isikukood_teistpidi; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_isikukood_teistpidi ON isikud USING btree (isikukood DESC NULLS LAST);


--
-- TOC entry 4760 (class 1259 OID 17353)
-- Name: ix_riiginimi; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_riiginimi ON riigid USING btree (nimi COLLATE "C");


--
-- TOC entry 4761 (class 1259 OID 17354)
-- Name: ix_suurus; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_suurus ON riigid USING btree (pindala DESC NULLS LAST, rahvaarv);


--
-- TOC entry 4759 (class 1259 OID 17355)
-- Name: partiid_turniir_valge_valge_tulemus_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX partiid_turniir_valge_valge_tulemus_idx ON partiid USING btree (turniir, valge, valge_tulemus);


--
-- TOC entry 4775 (class 2620 OID 17356)
-- Name: partiid tg_ajakontroll; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tg_ajakontroll AFTER INSERT OR UPDATE ON partiid FOR EACH ROW EXECUTE FUNCTION f_ajakontroll();


--
-- TOC entry 4776 (class 2620 OID 17357)
-- Name: partiid tg_ajakontroll1; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tg_ajakontroll1 AFTER INSERT ON partiid FOR EACH ROW EXECUTE FUNCTION f_ajakontroll1();


--
-- TOC entry 4773 (class 2620 OID 17358)
-- Name: isikud tg_klubi_olemasolu; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tg_klubi_olemasolu AFTER INSERT OR UPDATE ON isikud FOR EACH ROW EXECUTE FUNCTION f_kontrolli_klubi();


--
-- TOC entry 4774 (class 2620 OID 17359)
-- Name: klubid tg_kustuta_klubi; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tg_kustuta_klubi AFTER DELETE ON klubid FOR EACH ROW EXECUTE FUNCTION f_kontrolli_klubi_asulat();


--
-- TOC entry 4777 (class 2620 OID 17360)
-- Name: partiid tg_partiiaeg; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tg_partiiaeg BEFORE INSERT OR UPDATE ON partiid FOR EACH ROW EXECUTE FUNCTION f_partiiaeg_kontroll();


--
-- TOC entry 4778 (class 2620 OID 17361)
-- Name: riigid tg_riigid; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER tg_riigid BEFORE INSERT ON riigid FOR EACH ROW EXECUTE FUNCTION f_riigi_kontroll();


--
-- TOC entry 4768 (class 2606 OID 17362)
-- Name: isikud fk_isikud2klubid; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY isikud
    ADD CONSTRAINT fk_isikud2klubid FOREIGN KEY (klubi) REFERENCES klubid(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 4769 (class 2606 OID 17367)
-- Name: partiid fk_partiid2must; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY partiid
    ADD CONSTRAINT fk_partiid2must FOREIGN KEY (must) REFERENCES isikud(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 4770 (class 2606 OID 17372)
-- Name: partiid fk_partiid2turniirid; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY partiid
    ADD CONSTRAINT fk_partiid2turniirid FOREIGN KEY (turniir) REFERENCES turniirid(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4771 (class 2606 OID 17377)
-- Name: partiid fk_partiid2valge; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY partiid
    ADD CONSTRAINT fk_partiid2valge FOREIGN KEY (valge) REFERENCES isikud(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 4772 (class 2606 OID 17382)
-- Name: turniirid fk_turniir_2_asula; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY turniirid
    ADD CONSTRAINT fk_turniir_2_asula FOREIGN KEY (asula) REFERENCES asulad(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 4940 (class 0 OID 17266)
-- Dependencies: 224 4948
-- Name: mv_partiide_arv_valgetega; Type: MATERIALIZED VIEW DATA; Schema: public; Owner: -
--

REFRESH MATERIALIZED VIEW mv_partiide_arv_valgetega;


-- Completed on 2024-01-13 13:29:12

--
-- PostgreSQL database dump complete
--

