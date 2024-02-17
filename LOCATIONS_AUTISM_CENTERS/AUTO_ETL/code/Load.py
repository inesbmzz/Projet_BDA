import cx_Oracle
import sys

# Set up connection parameters
username = 'SID/Oracle21c'

# Establish a connection to the Oracle database
connection = cx_Oracle.connect(username)
cursor = connection.cursor()

# SQL script to execute
sql_script1 = """
BEGIN
   -- Attempt to drop the autism_screening table
   EXECUTE IMMEDIATE 'BEGIN EXECUTE IMMEDIATE ''DROP TABLE autism_screening PURGE''; EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF; END;';

   -- Attempt to drop the sequence
   EXECUTE IMMEDIATE 'BEGIN EXECUTE IMMEDIATE ''DROP SEQUENCE autism_screening_seq''; EXCEPTION WHEN OTHERS THEN IF SQLCODE != -2289 THEN RAISE; END IF; END;';

   -- Create Sequence for ID auto-increment
   EXECUTE IMMEDIATE 'CREATE SEQUENCE autism_screening_seq START WITH 1 INCREMENT BY 1';

   -- Create the autism_screening table
   EXECUTE IMMEDIATE '
   CREATE TABLE autism_screening (
       id NUMBER PRIMARY KEY,
       A1_Score NUMBER(1) CONSTRAINT A1_Score_chk CHECK (A1_Score BETWEEN 0 AND 1) NOT NULL,
       A2_Score NUMBER(1) CONSTRAINT A2_Score_chk CHECK (A2_Score BETWEEN 0 AND 1) NOT NULL,
       A3_Score NUMBER(1) CONSTRAINT A3_Score_chk CHECK (A3_Score BETWEEN 0 AND 1) NOT NULL,
       A4_Score NUMBER(1) CONSTRAINT A4_Score_chk CHECK (A4_Score BETWEEN 0 AND 1) NOT NULL,
       A5_Score NUMBER(1) CONSTRAINT A5_Score_chk CHECK (A5_Score BETWEEN 0 AND 1) NOT NULL,
       A6_Score NUMBER(1) CONSTRAINT A6_Score_chk CHECK (A6_Score BETWEEN 0 AND 1) NOT NULL,
       A7_Score NUMBER(1) CONSTRAINT A7_Score_chk CHECK (A7_Score BETWEEN 0 AND 1) NOT NULL,
       A8_Score NUMBER(1) CONSTRAINT A8_Score_chk CHECK (A8_Score BETWEEN 0 AND 1) NOT NULL,
       A9_Score NUMBER(1) CONSTRAINT A9_Score_chk CHECK (A9_Score BETWEEN 0 AND 1) NOT NULL,
       A10_Score NUMBER(1) CONSTRAINT A10_Score_chk CHECK (A10_Score BETWEEN 0 AND 1) NOT NULL,
       age FLOAT(126) CONSTRAINT age_chk CHECK (age > 0 AND age < 150) NOT NULL,
       gender CHAR(1) CONSTRAINT gender_chk CHECK (gender IN (''m'', ''f'')) NOT NULL,
       ethnicity VARCHAR2(50) NOT NULL,
       jaundice VARCHAR2(3) CONSTRAINT jaundice_chk CHECK (jaundice IN (''yes'', ''no'')) NOT NULL,
       autism VARCHAR2(3) CONSTRAINT autism_chk CHECK (autism IN (''yes'', ''no'')) NOT NULL,
       result FLOAT(126) CONSTRAINT result_chk CHECK (result >= 0) NOT NULL,
       relation VARCHAR2(50) NOT NULL,
       Class_ASD VARCHAR2(3) CONSTRAINT Class_ASD_chk CHECK (Class_ASD IN (''YES'', ''NO'')) NOT NULL
   )';

   -- Create triggers using EXECUTE IMMEDIATE
   EXECUTE IMMEDIATE '
   CREATE OR REPLACE TRIGGER autism_screening_id 
   BEFORE INSERT ON autism_screening 
   FOR EACH ROW
   BEGIN
     SELECT autism_screening_seq.NEXTVAL
     INTO   :new.id
     FROM   dual;
   END;';

   EXECUTE IMMEDIATE '
   CREATE OR REPLACE TRIGGER trg_before_insert_autism_screening
   BEFORE INSERT ON autism_screening
   FOR EACH ROW
   DECLARE
     v_exists NUMBER;
   BEGIN
     SELECT COUNT(*)
     INTO v_exists
     FROM autism_screening
     WHERE A1_Score = :new.A1_Score
       AND A2_Score = :new.A2_Score
       AND A3_Score = :new.A3_Score
       AND A4_Score = :new.A4_Score
       AND A5_Score = :new.A5_Score
       AND A6_Score = :new.A6_Score
       AND A7_Score = :new.A7_Score
       AND A8_Score = :new.A8_Score
       AND A9_Score = :new.A9_Score
       AND A10_Score = :new.A10_Score
       AND age = :new.age
       AND gender = :new.gender
       AND ethnicity = :new.ethnicity
       AND jaundice = :new.jaundice
       AND autism = :new.autism
       AND result = :new.result
       AND relation = :new.relation
       AND Class_ASD = :new.Class_ASD;
     IF v_exists > 0 THEN
       RAISE_APPLICATION_ERROR(-20001, ''Un enregistrement similaire existe déjà dans la table.'');
     END IF;
   END;';
END;
"""

sql_script2 = """
-- Récupère toutes les données de la table temporaire 'temp_centers'
SELECT * FROM temp_centers;

-- Extraction et insertion des données de temp_centers vers Countries,Cities, Centers
SET SERVEROUTPUT ON;
DECLARE
  -- Déclaration des variables
  v_PO_BOX VARCHAR2(255);
  v_street_name VARCHAR2(255);
  v_street_num VARCHAR2(255);
  v_district VARCHAR2(255);
  v_postal_code VARCHAR2(30);
  v_region VARCHAR2(255);
  v_city_id NUMBER;
  v_address T_ADRESSE;
  v_infos T_Informations;
  v_info_raw VARCHAR2(4000); -- Pour stocker les informations brutes de chaque enregistrement
  v_info_element VARCHAR2(400);
  v_element_index PLS_INTEGER;
BEGIN

 --  Insertion des pays uniques dans la table Countries
    INSERT INTO Countries (CountryName)
    SELECT DISTINCT country FROM temp_centers
    WHERE country NOT IN (SELECT CountryName FROM Countries);

    --  Insertion des villes uniques dans la table Cities
    INSERT INTO Cities (CityName, CountryID)
    SELECT DISTINCT t.city, c.CountryID
    FROM temp_centers t
    JOIN Countries c ON t.country = c.CountryName
    WHERE t.city NOT IN (SELECT CityName FROM Cities);
    
  FOR r IN (SELECT * FROM temp_centers) LOOP
     -- Extraction des composants de l'adresse
     v_PO_BOX := REGEXP_SUBSTR(r.address, '[^,]+', 1, 1); 
     v_street_name := REGEXP_SUBSTR(r.address,'[^,]+', 1, 2); 
     v_street_num := REGEXP_SUBSTR(r.address,'[^,]+', 1, 3);
     v_district := REGEXP_SUBSTR(r.address,'[^,]+', 1, 4); 
     v_postal_code := REGEXP_SUBSTR(r.address,'[^,]+', 1, 5);
     v_region := REGEXP_SUBSTR(r.address,'[^,]+', 1, 6); 
  
     -- Création de l'objet adresse
     v_address := T_ADRESSE(v_PO_BOX, v_street_name, v_street_num, v_district, v_postal_code, v_region);
  
     -- Affichage pour vérification
        DBMS_OUTPUT.PUT_LINE( 'PO box: ' || v_PO_BOX || ', Street Name: ' || v_street_name || ', Street Number: ' || v_street_num || ', District: ' || v_district || ', Postal Code: ' || v_postal_code || ', Region: ' || v_region);
      -- Réinitialisation des variables pour chaque enregistrement
    v_infos := T_Informations();
    v_element_index := 1;
    v_info_raw := r.info; 
    
    -- Séparation et ajout des informations dans la collection v_infos
    LOOP
      v_info_element := REGEXP_SUBSTR(v_info_raw, '[^,]+', 1, v_element_index);
      EXIT WHEN v_info_element IS NULL OR v_info_element = '';
      v_infos.EXTEND;
      v_infos(v_infos.LAST) := TRIM(v_info_element);
      v_element_index := v_element_index + 1;
    END LOOP;
    
    -- Recherche du cityId basé sur le nom de la ville et du pays
    SELECT ci.CityID INTO v_city_id
    FROM Cities ci
    JOIN Countries co ON ci.CountryID = co.CountryID
    WHERE ci.CityName = r.city AND co.CountryName = r.country;
    
    -- Insérer les données dans Centers
    INSERT INTO Centers (name, latitude, longitude, address, cityId, infos)
    VALUES (r.name, r.latitude, r.longitude, v_address, v_city_id, v_infos);
  END LOOP;
  COMMIT;
END;
/

-- Récupère toutes les entrées de la table 'Countries' pour afficher les pays disponibles
SELECT * FROM Countries;

-- Récupère toutes les entrées de la table 'Cities' pour afficher cities disponibles
SELECT * FROM Cities;

-- Récupère toutes les entrées de la table 'Centers' pour afficher les centres disponibles
SELECT * FROM Centers;

-- Sélectionne plusieurs champs de la table 'Centers', en décomposant l'objet adresse stocké
-- pour afficher ses composants de manière plus lisible et structurée
SELECT 
    c.id_Centers,
    c.address.PO_BOX AS Post_office_box,
    c.address.Street_name AS StreetName,
    c.address.Street_num AS StreetNumber,
    c.address.District AS District,
    c.address.Code_postal AS PostalCode,
    c.address.Region AS Region
FROM 
    Centers c;

-- Extrait chaque élément de la collection d'informations stockée dans 'infos' pour chaque centre
-- et les affiche de manière tabulaire, associant chaque information à l'ID du centre correspondant
SELECT c.id_Centers, i.column_value AS information
FROM Centers c,
TABLE(c.infos) i;

-- Supprime la table temporaire 'temp_centers' après son utilisation
-- Cela est souvent fait pour nettoyer et libérer de l'espace dans la base de données
DROP TABLE temp_centers;

-- Faire un join des 3 tables
SELECT
    cnt.CountryName,
    cty.CityName,
    ctr.name AS CenterName,
    ctr.latitude,
    ctr.longitude,
    -- Concaténation des champs de l'adresse en une chaîne de caractères
    ctr.address.PO_BOX || ctr.address.Street_name || ctr.address.Street_num ||
    ctr.address.District ||ctr.address.Code_postal || ctr.address.Region 
    AS FullAddress,
    -- Extraction et concaténation des informations
    (SELECT LISTAGG(info.column_value, ', ') WITHIN GROUP (ORDER BY info.column_value)
     FROM TABLE(ctr.infos) info) AS InformationList
FROM
    Centers ctr
JOIN Cities cty ON ctr.cityId = cty.CityID
JOIN Countries cnt ON cty.CountryID = cnt.CountryID;
"""

args = sys.argv
sql_script = sql_script1 if args[1] == '1' else sql_script2

# Execute the SQL script
cursor.execute(sql_script)

# Commit the changes
connection.commit()

# Close cursor and connection
cursor.close()
connection.close()
