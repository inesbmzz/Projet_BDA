-- ************************************************TEST UNITAIRE ********************************
SET SERVEROUTPUT ON;
DECLARE
  -- Variables pour stocker les valeurs de test
  v_test_id NUMBER;
  v_A1_Score NUMBER(1) := 1;
  v_A2_Score NUMBER(1) := 0;
  v_A3_Score NUMBER(1) := 0;
  v_A4_Score NUMBER(1) := 1;
  v_A5_Score NUMBER(1) := 0;
  v_A6_Score NUMBER(1) := 1;
  v_A7_Score NUMBER(1) := 1;
  v_A8_Score NUMBER(1) := 0;
  v_A9_Score NUMBER(1) := 0;
  v_A10_Score NUMBER(1) := 1;
  v_age NUMBERS := 21;
  v_gender CHAR(1) := 'f';
  v_ethnicity VARCHAR2(50) := 'Test Ethnicity';
  v_jaundice VARCHAR2(3) := 'no';
  v_autism VARCHAR2(3) := 'no';
  v_result FLOAT := 5;
  v_relation VARCHAR2(50) := 'Self';
  v_Class_ASD VARCHAR2(3) := 'NO';
BEGIN
  -- Insertion de données de test
  INSERT INTO autism_screening (A1_Score, A2_Score, A3_Score, A4_Score, A5_Score, A6_Score, A7_Score, A8_Score, A9_Score, A10_Score, age, gender, ethnicity, jaundice, autism, result, relation, Class_ASD)
  VALUES (v_A1_Score, v_A2_Score, v_A3_Score, v_A4_Score, v_A5_Score, v_A6_Score, v_A7_Score, v_A8_Score, v_A9_Score, v_A10_Score, v_age, v_gender, v_ethnicity, v_jaundice, v_autism, v_result, v_relation, v_Class_ASD)
  RETURNING id INTO v_test_id;

  DBMS_OUTPUT.PUT_LINE('Insertion réussie. ID de test: ' || v_test_id);

  -- Tentative d'insertion de données dupliquées pour tester le trigger
  BEGIN
    INSERT INTO autism_screening (A1_Score, A2_Score, A3_Score, A4_Score, A5_Score, A6_Score, A7_Score, A8_Score, A9_Score, A10_Score, age, gender, ethnicity, jaundice, autism, result, relation, Class_ASD)
    VALUES (v_A1_Score, v_A2_Score, v_A3_Score, v_A4_Score, v_A5_Score, v_A6_Score, v_A7_Score, v_A8_Score, v_A9_Score, v_A10_Score, v_age, v_gender, v_ethnicity, v_jaundice, v_autism, v_result, v_relation, v_Class_ASD);
    DBMS_OUTPUT.PUT_LINE('Échec du test: Insertion de données dupliquées réussie.');
  EXCEPTION
    WHEN OTHERS THEN
      DBMS_OUTPUT.PUT_LINE('Succès du test: L''insertion de données dupliquées a échoué comme prévu.');
  END;

  -- Nettoyage: Suppression des données de test insérées
  DELETE FROM autism_screening WHERE id = v_test_id;
  DBMS_OUTPUT.PUT_LINE('Nettoyage réussi. Données de test supprimées.');

EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Erreur lors de l''exécution du test: ' || SQLERRM);
END;
/

-- Test d'Existence des Tables ******************************************************************************************
SELECT table_name FROM user_tables WHERE table_name IN ('AUTISM_SCREENING');

-- Test des Colonnes et Types **********************************************************************************

SELECT column_name, data_type FROM user_tab_columns WHERE table_name = 'AUTISM_SCREENING';

