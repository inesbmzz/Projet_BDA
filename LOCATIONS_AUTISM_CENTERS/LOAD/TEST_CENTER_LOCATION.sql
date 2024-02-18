-- ***********************************************************TEST UNITAIRE *********************************************************
-- Test Unitaire pour la Table Countries
-- V�rifier que l'insertion d'un nouveau pays fonctionne correctement et que ce pays peut �tre r�cup�r�.
-- Cr�ation du package de test
CREATE OR REPLACE PACKAGE test_countries_pkg IS
   -- Proc�dure de test pour l'insertion et la s�lection dans la table Countries
   PROCEDURE test_insert_and_select_country;
END test_countries_pkg;
/

CREATE OR REPLACE PACKAGE BODY test_countries_pkg IS
   PROCEDURE test_insert_and_select_country IS
      v_country_name VARCHAR2(255) := 'TestCountry';
      v_country_id NUMBER;
      v_count NUMBER;
   BEGIN
      -- Insertion d'un test country
      INSERT INTO Countries (CountryName) VALUES (v_country_name);
      
      -- R�cup�ration de l'ID du pays ins�r�
      SELECT CountryID INTO v_country_id FROM Countries WHERE CountryName = v_country_name;
      
      -- V�rification que l'ID du pays r�cup�r� est sup�rieur � 0
      IF v_country_id IS NULL THEN
         RAISE_APPLICATION_ERROR(-20001, 'Test �chou� : Aucun ID r�cup�r� pour le pays ins�r�.');
      END IF;
      
      -- Compter le nombre d'occurrences du pays ins�r�
      SELECT COUNT(*) INTO v_count FROM Countries WHERE CountryID = v_country_id;
      
      -- V�rification que le pays ins�r� existe bien
      IF v_count != 1 THEN
         RAISE_APPLICATION_ERROR(-20002, 'Test �chou� : Le pays ins�r� n''existe pas dans la table.');
      ELSE
         DBMS_OUTPUT.PUT_LINE('Test r�ussi : Le pays a �t� correctement ins�r� et v�rifi�.');
      END IF;
      
      -- Nettoyage apr�s test
      DELETE FROM Countries WHERE CountryID = v_country_id;
      COMMIT;
   END test_insert_and_select_country;
END test_countries_pkg;
/
BEGIN
   test_countries_pkg.test_insert_and_select_country;
END;
/
--  Test unitaire  pour la Table Centers ****************

DECLARE
  v_country_id NUMBER;
  v_fake_country_id NUMBER := -1; -- Un ID qui n'existe pas
  v_city_name_valid VARCHAR2(255) := 'Test City';
  v_city_name_invalid VARCHAR2(255) := 'Fail City';
  v_inserted_city_id NUMBER;
BEGIN
  -- Test 1: Insertion d'une nouvelle ville avec un ID de pays valide
  BEGIN
    SELECT CountryID INTO v_country_id FROM Countries WHERE ROWNUM = 1;
    
    INSERT INTO Cities (CityName, CountryID) VALUES (v_city_name_valid, v_country_id) RETURNING CityID INTO v_inserted_city_id;
    DBMS_OUTPUT.PUT_LINE('Test 1 Pass: Ville correctement ins�r�e avec ID ' || v_inserted_city_id || '.');
    
    -- Suppression de la ville ins�r�e pour nettoyer
    DELETE FROM Cities WHERE CityID = v_inserted_city_id;
    DBMS_OUTPUT.PUT_LINE('Nettoyage: Ville avec ID ' || v_inserted_city_id || ' supprim�e.');
    
  EXCEPTION
    WHEN NO_DATA_FOUND THEN
      DBMS_OUTPUT.PUT_LINE('Erreur: Aucun pays trouv� pour tester l''insertion.');
    WHEN OTHERS THEN
      DBMS_OUTPUT.PUT_LINE('Test 1 Fail: Erreur lors de l''insertion de la ville.');
  END;
  
  -- Test 2: Tentative d'insertion d'une ville avec un ID de pays invalide
  BEGIN
    INSERT INTO Cities (CityName, CountryID) VALUES (v_city_name_invalid, v_fake_country_id);
    DBMS_OUTPUT.PUT_LINE('Test 2 Fail: Insertion r�ussie avec un ID de pays invalide.');
  EXCEPTION
    WHEN OTHERS THEN
      DBMS_OUTPUT.PUT_LINE('Test 2 Pass: �chec de l''insertion comme pr�vu en raison d''un ID de pays invalide.');
  END;
END;
/

-- Test unitaire de la tables Centers*********************************************************

DECLARE
  v_city_id NUMBER;
  v_center_name VARCHAR2(255) := 'Test Center';
  v_latitude_valid FLOAT := 48.8566; -- Latitude valide pour Paris
  v_longitude_valid FLOAT := 2.3522; -- Longitude valide pour Paris
  v_latitude_invalid FLOAT := 100.0; -- Latitude invalide
  v_longitude_invalid FLOAT := 200.0; -- Longitude invalide
  v_inserted_center_id NUMBER;
  v_address T_ADRESSE := T_ADRESSE('123', 'Test Street', '10', 'Test District', '10000', 'Test Region');
  v_infos T_Informations := T_Informations('Info1', 'Info2');
BEGIN
  -- Assurer qu'une ville existe pour l'exemple
  SELECT CityID INTO v_city_id FROM Cities WHERE ROWNUM = 1;
  
  -- Test 1: Insertion d'un nouveau centre avec des donn�es valides
  BEGIN
    INSERT INTO Centers (name, latitude, longitude, address, cityId, infos)
    VALUES (v_center_name, v_latitude_valid, v_longitude_valid, v_address, v_city_id, v_infos)
    RETURNING id_Centers INTO v_inserted_center_id;
    
    DBMS_OUTPUT.PUT_LINE('Test 1 Pass: Centre correctement ins�r� avec ID ' || v_inserted_center_id || '.');
    
    -- Suppression du centre ins�r� pour nettoyer
    DELETE FROM Centers WHERE id_Centers = v_inserted_center_id;
    DBMS_OUTPUT.PUT_LINE('Nettoyage: Centre avec ID ' || v_inserted_center_id || ' supprim�.');
  EXCEPTION
    WHEN NO_DATA_FOUND THEN
      DBMS_OUTPUT.PUT_LINE('Erreur: Aucune ville trouv�e pour tester l''insertion.');
    WHEN OTHERS THEN
      DBMS_OUTPUT.PUT_LINE('Test 1 Fail: Erreur lors de l''insertion du centre.');
  END;
  
  -- Test 2: Tentative d'insertion d'un centre avec des donn�es g�ographiques invalides
  BEGIN
    INSERT INTO Centers (name, latitude, longitude, address, cityId, infos)
    VALUES (v_center_name, v_latitude_invalid, v_longitude_invalid, v_address, v_city_id, v_infos);
    
    DBMS_OUTPUT.PUT_LINE('Test 2 Fail: Insertion r�ussie avec des donn�es g�ographiques invalides.');
  EXCEPTION
    WHEN OTHERS THEN
      DBMS_OUTPUT.PUT_LINE('Test 2 Pass: �chec de l''insertion comme pr�vu en raison de donn�es g�ographiques invalides.');
  END;
END;
/


-- *******************************************************Metadata Testing ****************************************************

-- Test de les S�quences ***********************************************************************************************
CREATE OR REPLACE PROCEDURE test_sequences IS
  v_test_country_id NUMBER;
  v_test_city_id NUMBER;
  v_test_center_id NUMBER;
BEGIN
  -- Test pour country_seq
  INSERT INTO Countries (CountryName) VALUES ('TestCountrySeq');
  SELECT country_seq.CURRVAL INTO v_test_country_id FROM dual;
  DBMS_OUTPUT.PUT_LINE('Test Country ID (country_seq): ' || v_test_country_id);

  -- Test pour city_seq
  INSERT INTO Cities (CityName, CountryID) VALUES ('TestCitySeq', v_test_country_id);
  SELECT city_seq.CURRVAL INTO v_test_city_id FROM dual;
  DBMS_OUTPUT.PUT_LINE('Test City ID (city_seq): ' || v_test_city_id);

  -- Test pour center_seq
  INSERT INTO Centers (name, latitude, longitude, address, cityId, infos) VALUES 
    ('TestCenterSeq', 0, 0, T_ADRESSE('','','','','',''), v_test_city_id, T_Informations());
  SELECT center_seq.CURRVAL INTO v_test_center_id FROM dual;
  DBMS_OUTPUT.PUT_LINE('Test Center ID (center_seq): ' || v_test_center_id);

  COMMIT;
EXCEPTION
  WHEN OTHERS THEN
    -- Gestion des erreurs
    DBMS_OUTPUT.PUT_LINE('Erreur: ' || SQLERRM);
    ROLLBACK;
END;
/

SET SERVEROUTPUT ON;
EXEC test_sequences;


-- Test d'Existence des Tables ******************************************************************************************
SELECT table_name FROM user_tables WHERE table_name IN ('COUNTRIES', 'CITIES', 'CENTERS');

-- Test des Colonnes et Types **********************************************************************************

-- Pour Countries
SELECT column_name, data_type FROM user_tab_columns WHERE table_name = 'COUNTRIES';

-- Pour Cities
SELECT column_name, data_type FROM user_tab_columns WHERE table_name = 'CITIES';

-- Pour Centers
SELECT column_name, data_type FROM user_tab_columns WHERE table_name = 'CENTERS';


-- Contraintes de Cl� �trang�re
-- Pour Cities avec un CountryID inexistant
INSERT INTO Cities (CityName, CountryID) VALUES ('NoCountryCity', 9999);

-- Pour Centers avec un CityID inexistant
INSERT INTO Centers (name, latitude, longitude, address, cityId) VALUES ('NoCityCenter', 0, 0, T_ADRESSE('','','','','',''), 9999);


-- Contraintes Uniques
-- Pour Countries
INSERT INTO Countries (CountryName) VALUES ('UniqueCountry');
INSERT INTO Countries (CountryName) VALUES ('UniqueCountry');


-- Contraintes de V�rification
-- Pour Centers (latitude hors de port�e)
INSERT INTO Centers (name, latitude, longitude, address, cityId) VALUES ('BadLat', -91, 0, T_ADRESSE('','','','','',''), 1);
INSERT INTO Centers (name, latitude, longitude, address, cityId) VALUES ('BadLat', 91, 0, T_ADRESSE('','','','','',''), 1);

-- Pour Centers (longitude hors de port�e)
INSERT INTO Centers (name, latitude, longitude, address, cityId) VALUES ('BadLong', 0, -181, T_ADRESSE('','','','','',''), 1);
INSERT INTO Centers (name, latitude, longitude, address, cityId) VALUES ('BadLong', 0, 181, T_ADRESSE('','','','','',''), 1);


