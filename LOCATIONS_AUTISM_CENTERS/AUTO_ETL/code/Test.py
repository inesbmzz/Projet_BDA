import pandas as pd
import re

# Testing of the autism_treatment_centers_autism_now.csv file

# Read the CSV file
dan = pd.read_csv("data/autism_treatment_centers_autism_now_processed.csv")

tests_passed = True

# Verify the format of info column (Contact info)
regex = r'[\w\.-]+@[\w\.-]+\.\w+|\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}'

infos_errors = []
for i in range(len(dan)):
    if pd.isna(dan["info"][i]):
        continue
    for info in dan["info"][i].split(", "):
        if not re.match(regex, info):
            infos_errors.append([i+1, info])
            tests_passed = False

if len(infos_errors) > 0:
    print(f"❌ Test failed for info column in rows:")
    for error in infos_errors:
        print(f"\t- row {error[0]}: '{error[1]}' is not a valid email or phone number")

# Verify the format of the address column
addresses_errors = []
for i in range(len(dan)):
    if pd.isna(dan["address"][i]):
        tests_passed = False
        addresses_errors.append([i+1, "No address provided"])
        continue

    elements: list[str] = dan["address"][i].split(",")
    if elements[0] != " " and not elements[0].isdigit():
        tests_passed = False
        addresses_errors.append([i+1, f"'{elements[0]}' is not a valid PO Box"])

    if elements[1] == " " and elements[2] != " ":
        tests_passed = False
        addresses_errors.append([i+1, f"Street number '{elements[2]}' without street name"])

    if elements[1] != " " and elements[2] == " ":
        tests_passed = False
        addresses_errors.append([i+1, f"Street name '{elements[1]}' without street number"])

    if elements[2] != " " and not elements[2].isdigit():
        tests_passed = False
        addresses_errors.append([i+1, f"'{elements[2]}' is not a valid street number"])

    if elements[3] == " ":
        tests_passed = False
        addresses_errors.append([i+1, "No city provided"])

    if elements[4] == " ":
        tests_passed = False
        addresses_errors.append([i+1, f'No valid zip code'])

    if elements[4] != " " and any(not part.isdigit() for part in elements[4].split("-")):
        tests_passed = False
        addresses_errors.append([i+1, f"'{elements[4]}' is not a valid zip code"])

    if elements[5] == " ":
        tests_passed = False
        addresses_errors.append([i+1, "No county provided"])

if len(addresses_errors) > 0:
    print(f"❌ Test failed for address column in rows:")
    for error in addresses_errors:
        print(f"\t- row {error[0]}: {error[1]}")

# Verify that country is always USA
countries_errors = []
for i in range(len(dan)):
    if dan["country"][i] != "USA":
        tests_passed = False
        countries_errors.append(i+1)

if len(countries_errors) > 0:
    print(f"❌ Test failed for country column in rows:")
    for error in countries_errors:
        print(f"\t- row {error}: Country is not USA")

# Verify that the states are valid
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

states_errors = []
for i in range(len(dan)):
    if dan["city"][i] not in us_state_to_abbrev.keys():
        tests_passed = False
        states_errors.append([i+1, dan["city"][i]])

if len(states_errors) > 0:
    print(f"❌ Test failed for state column in rows:")
    for error in states_errors:
        print(f"\t- row {error[0]}: '{error[1]}' is not a valid US state")