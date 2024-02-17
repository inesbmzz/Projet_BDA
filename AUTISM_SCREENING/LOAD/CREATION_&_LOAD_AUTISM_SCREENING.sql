-- Suppression des tables avec vérification de l'existence
BEGIN
   -- Tentative de suppression de la table autism_screening
   EXECUTE IMMEDIATE 'DROP TABLE autism_screening ';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE != -942 THEN
         RAISE;
      END IF;
END;
/

-- Supression des séquences 
DROP SEQUENCE autism_screening_seq;

--Création de Séquence Pour l'auto-incrémentation d'identifiants
CREATE SEQUENCE autism_screening_seq START WITH 1 INCREMENT BY 1;

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
    gender CHAR(1) CONSTRAINT gender_chk CHECK (gender IN ('m', 'f')) NOT NULL,
    ethnicity VARCHAR2(50) NOT NULL,
    jaundice VARCHAR2(3) CONSTRAINT jaundice_chk CHECK (jaundice IN ('yes', 'no')) NOT NULL,
    autism VARCHAR2(3) CONSTRAINT autism_chk CHECK (autism IN ('yes', 'no')) NOT NULL,
    result FLOAT(126) CONSTRAINT result_chk CHECK (result >= 0) NOT NULL,
    relation VARCHAR2(50) NOT NULL,
    Class_ASD VARCHAR2(3) CONSTRAINT Class_ASD_chk CHECK (Class_ASD IN ('YES', 'NO')) NOT NULL
);

CREATE OR REPLACE TRIGGER autism_screening_id 
BEFORE INSERT ON autism_screening 
FOR EACH ROW
BEGIN
  SELECT autism_screening_seq.NEXTVAL
  INTO   :new.id
  FROM   dual;
END;
/

CREATE OR REPLACE TRIGGER trg_before_insert_autism_screening
BEFORE INSERT ON autism_screening
FOR EACH ROW
DECLARE
  v_exists NUMBER;
BEGIN
  -- Vérifie l'existence d'un enregistrement avec les mêmes valeurs pour toutes les colonnes
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
    -- Annule l'insertion si un enregistrement similaire existe déjà
    RAISE_APPLICATION_ERROR(-20001, 'Un enregistrement similaire existe déjà dans la table.');
  END IF;
END;
/

SELECT * FROM autism_screening;
