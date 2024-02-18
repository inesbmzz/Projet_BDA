import cx_Oracle
import sys

# Set up connection parameters
username = 'SID/Oracle21c'

# Establish a connection to the Oracle database
connection = cx_Oracle.connect(username)
cursor = connection.cursor()

# SQL script to execute
sql_script1 = """
-- Suppression des tables avec vérification de l'existence
BEGIN
   -- Tentative de suppression de la table Countries
   EXECUTE IMMEDIATE 'DROP TABLE Countries CASCADE CONSTRAINTS';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE != -942 THEN
         RAISE;
      END IF;
END;
/

BEGIN
   -- Tentative de suppression de la table Cities
   EXECUTE IMMEDIATE 'DROP TABLE Cities CASCADE CONSTRAINTS';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE != -942 THEN
         RAISE;
      END IF;
END;
/

BEGIN
   -- Tentative de suppression de la table Centers
   EXECUTE IMMEDIATE 'DROP TABLE Centers';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE != -942 THEN
         RAISE;
      END IF;
END;
/
-- Supression des séquences 
DROP SEQUENCE country_seq;
DROP SEQUENCE city_seq;
DROP SEQUENCE center_seq;

--Création des Séquences Pour l'auto-incrémentation des identifiants 
CREATE SEQUENCE country_seq START WITH 1 INCREMENT BY 1 CACHE 100;
CREATE SEQUENCE city_seq START WITH 1 INCREMENT BY 1 CACHE 100;
CREATE SEQUENCE center_seq START WITH 1 INCREMENT BY 1 NOCACHE;


--Création des Tables

CREATE TABLE Countries (
    CountryID NUMBER NOT NULL,
    CountryName VARCHAR2(255) NOT NULL,
    CONSTRAINT pk_countries PRIMARY KEY (CountryID)
);

CREATE TABLE Cities (
    CityID NUMBER NOT NULL,
    CityName VARCHAR2(255) NOT NULL,
    CountryID NUMBER,
    CONSTRAINT pk_cities PRIMARY KEY (CityID),
    CONSTRAINT fk_country FOREIGN KEY (CountryID) REFERENCES Countries(CountryID)
);
-- Création du type adresse
CREATE OR REPLACE TYPE T_ADRESSE AS OBJECT (
    PO_BOX VARCHAR2(255),
    Street_num VARCHAR(255),
    District  VARCHAR(255), 
    Street_name VARCHAR(255),
    Code_postal VARCHAR(30),
    Region VARCHAR(255)
);
/
-- Définir le type pour les informations (Nested Table)
CREATE OR REPLACE TYPE T_Informations AS TABLE OF VARCHAR(400);
/

-- Création de la table Centers
CREATE TABLE Centers (
    id_Centers INT PRIMARY KEY,
    name VARCHAR(255),
    latitude FLOAT(126),
    longitude FLOAT(126),
    address T_ADRESSE,
    cityId NUMBER,
    infos T_Informations,
    CONSTRAINT fk_city FOREIGN KEY (cityId) REFERENCES Cities(CityID),
    CONSTRAINT chk_latitude CHECK (latitude BETWEEN -90 AND 90),
    CONSTRAINT chk_longitude CHECK (longitude BETWEEN -180 AND 180)
) NESTED TABLE infos STORE AS InfoTable;

-- Création des Triggers pour l'Auto-Incrémentation
CREATE OR REPLACE TRIGGER trg_country_id
BEFORE INSERT ON Countries
FOR EACH ROW
BEGIN
  SELECT country_seq.NEXTVAL INTO :new.CountryID FROM dual;
END;
/

CREATE OR REPLACE TRIGGER trg_city_id
BEFORE INSERT ON Cities
FOR EACH ROW
BEGIN
  SELECT city_seq.NEXTVAL INTO :new.CityID FROM dual;
END;
/

CREATE OR REPLACE TRIGGER trg_center_id
BEFORE INSERT ON Centers
FOR EACH ROW
BEGIN
  SELECT center_seq.NEXTVAL INTO :new.id_Centers FROM dual;
END;
/
-- Création de la table Centers
ALTER TABLE Countries ADD CONSTRAINT uniq_countryname UNIQUE (CountryName);

-- Création de la table temporaire pour les données initiales
CREATE TABLE temp_centers (
    name VARCHAR2(255),
    city VARCHAR2(255),
    country VARCHAR2(255),
    address VARCHAR2(400),
    latitude  REAL,
    longitude REAL,
    info VARCHAR2(4000),
    FREE_QUOTE_LINK VARCHAR(2055) DEFAULT ''
);
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

# Execute the SQL script
if sys.argv[1] == '1':
  # scripts = sql_script1.replace("/", "/ //").split('//')
  # scripts = sql_script1.split('/')
  cursor.execute(sql_script1)
  # print(len(scripts))
  # for part in scripts:
  #   try:
  #     cursor.execute(part.strip())
  #   except Exception as e:
  #     print(e)
  #     print(part.strip())
  #     break
else:
  cursor.execute(sql_script2)

# Commit the changes
connection.commit()

# Close cursor and connection
cursor.close()
connection.close()
