-- Cr�ation de la table temporaire pour les donn�es initiales
CREATE TABLE temp_centers (
    name VARCHAR2(255),
    city VARCHAR2(255),
    country VARCHAR2(255),
    address VARCHAR2(400),
    latitude  REAL,
    longitude REAL,
    info VARCHAR2(4000),
    FREE_QUOTE_LINK VARCHAR(3000) DEFAULT ''
);

-- R�cup�re toutes les donn�es de la table temporaire 'temp_centers'
SELECT * FROM temp_centers;

-- Extraction et insertion des donn�es de temp_centers vers Countries,Cities, Centers
SET SERVEROUTPUT ON;
DECLARE
  -- D�claration des variables
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
  
     -- Cr�ation de l'objet adresse
     v_address := T_ADRESSE(v_PO_BOX, v_street_name, v_street_num, v_district, v_postal_code, v_region);
  
     -- Affichage pour v�rification
        DBMS_OUTPUT.PUT_LINE( 'PO box: ' || v_PO_BOX || ', Street Name: ' || v_street_name || ', Street Number: ' || v_street_num || ', District: ' || v_district || ', Postal Code: ' || v_postal_code || ', Region: ' || v_region);
      -- R�initialisation des variables pour chaque enregistrement
    v_infos := T_Informations();
    v_element_index := 1;
    v_info_raw := r.info; 
    
    -- S�paration et ajout des informations dans la collection v_infos
    LOOP
      v_info_element := REGEXP_SUBSTR(v_info_raw, '[^,]+', 1, v_element_index);
      EXIT WHEN v_info_element IS NULL OR v_info_element = '';
      v_infos.EXTEND;
      v_infos(v_infos.LAST) := TRIM(v_info_element);
      v_element_index := v_element_index + 1;
    END LOOP;
    
    -- Recherche du cityId bas� sur le nom de la ville et du pays
    SELECT ci.CityID INTO v_city_id
    FROM Cities ci
    JOIN Countries co ON ci.CountryID = co.CountryID
    WHERE ci.CityName = r.city AND co.CountryName = r.country;
    
    -- Ins�rer les donn�es dans Centers
    INSERT INTO Centers (name, latitude, longitude, address, cityId, infos,free_quote_link)
    VALUES (r.name, r.latitude, r.longitude, v_address, v_city_id, v_infos,r.FREE_QUOTE_LINK);
  END LOOP;
  COMMIT;
END;
/



-- R�cup�re toutes les entr�es de la table 'Countries' pour afficher les pays disponibles
SELECT * FROM Countries;

-- R�cup�re toutes les entr�es de la table 'Cities' pour afficher cities disponibles
SELECT * FROM Cities;

-- R�cup�re toutes les entr�es de la table 'Centers' pour afficher les centres disponibles
SELECT * FROM Centers;

-- S�lectionne plusieurs champs de la table 'Centers', en d�composant l'objet adresse stock�
-- pour afficher ses composants de mani�re plus lisible et structur�e
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

-- Extrait chaque �l�ment de la collection d'informations stock�e dans 'infos' pour chaque centre
-- et les affiche de mani�re tabulaire, associant chaque information � l'ID du centre correspondant
SELECT c.id_Centers, i.column_value AS information
FROM Centers c,
TABLE(c.infos) i;

-- Supprime la table temporaire 'temp_centers' apr�s son utilisation
-- Cela est souvent fait pour nettoyer et lib�rer de l'espace dans la base de donn�es
DROP TABLE temp_centers;

-- Faire un join des 3 tables
SELECT
    cnt.CountryName,
    cty.CityName,
    ctr.name AS CenterName,
    ctr.latitude,
    ctr.longitude,
    -- Concat�nation des champs de l'adresse en une cha�ne de caract�res
    ctr.address.PO_BOX || ctr.address.Street_name || ctr.address.Street_num ||
    ctr.address.District ||ctr.address.Code_postal || ctr.address.Region 
    AS FullAddress,
    -- Extraction et concat�nation des informations
    (SELECT LISTAGG(info.column_value, ', ') WITHIN GROUP (ORDER BY info.column_value)
     FROM TABLE(ctr.infos) info) AS InformationList,
     ctr.free_quote_link
FROM
    Centers ctr
JOIN Cities cty ON ctr.cityId = cty.CityID
JOIN Countries cnt ON cty.CountryID = cnt.CountryID;

