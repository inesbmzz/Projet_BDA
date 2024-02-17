LOAD DATA
CHARACTERSET AL32UTF8
INFILE 'data\\autism_center.csv'
INTO TABLE TEMP_CENTERS
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    name,
    country,
    city,
    address,
    latitude "TO_NUMBER(:latitude, '9999.99999999999999999', 'NLS_NUMERIC_CHARACTERS=''.,''')",
    longitude "TO_NUMBER(:longitude, '9999.9999999999999999', 'NLS_NUMERIC_CHARACTERS=''.,''')",
    info,
    free_quote_link
)