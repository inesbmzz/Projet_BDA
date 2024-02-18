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
           Street_name VARCHAR(255),
           Street_num VARCHAR(255),
           District  VARCHAR(255), 
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
    free_quote_link VARCHAR(3000),
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
