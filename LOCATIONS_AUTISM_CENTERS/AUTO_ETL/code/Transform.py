import pandas as pd
import re

# Processing of the autism_treatment_centers_autism_now.csv file

# Read the CSV file
dan = pd.read_csv("data/autism_treatment_centers_autism_now_full.csv")

# Fix errors in some "contact info" values
dan['contact info'] = dan['contact info'].str.replace(' or By Website', '')
dan['contact info'] = dan['contact info'].replace('By Website', None)
dan['contact info'] = dan['contact info'].str.replace('770-904- 4474', '770-904-4474')

# Remove the Clinic name from the contact info
def remove_name_from_contact(contact_info, name):
    contact_info = contact_info.replace(name, "").strip() if contact_info is not None else None
    return contact_info
dan['contact info'] = dan.apply(lambda x: remove_name_from_contact(x['contact info'], x['name']), axis=1)

# Move phone numbers and emails to a new "info" column
def extract_phone_email(row, contact_info):
    if contact_info is None:
        return row
    regex = r'[\w\.-]+@[\w\.-]+\.\w+|\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}'
    phone_email = re.findall(regex, contact_info)
    row['info'] = ", ".join(phone_email)
    row['contact info'] = re.sub(regex, "", contact_info).strip()
    return row
dan = dan.apply(lambda x: extract_phone_email(x, x['contact info']), axis=1)
dan['contact info'] = dan['contact info'].str.replace("\r\n", ", ").str.replace("\n", ", ").str.strip()

# Rename "contact info" to "address"
dan = dan.rename(columns={'contact info': 'address'})

# Fix errors in some "address" and "city" values
dan['city'] = dan['city'].str.replace('San Bernadino', 'San Bernardino')
dan['address'] = dan['address'].str.replace(', California', ', CA')
dan['address'] = dan['address'].str.replace(', Grand Jct,', ', Grand Junction,')
dan['address'] = dan['address'].str.replace(', Colorado Spgs,', ', Colorado Springs,')
dan['address'] = dan['address'].str.replace(', Ft Walton Bch,', ', Fort Walton Beach,')
dan['address'] = dan['address'].str.replace(', Pt Charlotte,', ', Port Charlotte,')
dan['address'] = dan['address'].str.replace(', St Augustine,', ', St. Augustine,')
dan['address'] = dan['address'].str.replace(', Ft Lauderdale,', ', Fort Lauderdale,')
dan['address'] = dan['address'].str.replace(', Defuniak Spgs,', ', Defuniak Springs,')
dan['address'] = dan['address'].str.replace(', Chicago Hts,', ', Chicago Heights,')
dan['address'] = dan['address'].str.replace(', Donaldsonvlle,', ', Donaldsonville,')
dan['address'] = dan['address'].str.replace(', St Martinvlle,', ', St. Martinville,')
dan['address'] = dan['address'].str.replace(', N Weymouth,', ', North Weymouth,')
dan['address'] = dan['address'].str.replace(', Clinton Twp,', ', Clinton Township,')
dan['address'] = dan['address'].str.replace(', Mt Pleasant,', ', Mount Pleasant,')
dan['address'] = dan['address'].str.replace(', Saint Paul,', ', St. Paul,')
dan['address'] = dan['address'].str.replace(', Saint Cloud,', ', St. Cloud,')
dan['address'] = dan['address'].str.replace(', Saint Louis,', ', St. Louis,')
dan['address'] = dan['address'].str.replace(', N Brunswick,', ', North Brunswick,')
dan['city'] = dan['city'].str.replace('Mounty Airy', 'Mount Airy')
dan['address'] = dan['address'].str.replace(', Winston Salem,', ', Winston-Salem,')
dan['address'] = dan['address'].str.replace(', N Providence,', ', North Providence,')
dan['address'] = dan['address'].str.replace(', Fredericksbrg,', ', Fredericksburg,')
dan['address'] = dan['address'].str.replace(', St George,', ', St. George,')
dan['city'] = dan['city'].str.replace('Saint George', 'St. George')
dan['address'] = dan['address'].str.replace(', Richland Ctr,', ', Richland Center,')

# State -> Abbreviation dictionary
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

# Fix the "address" column format
def fix_address_format(state: str, county: str, city: str, address: str):
    # If the address is empty, return None
    if not address:
        return None
    
    # Split the address into elements
    address_elements = address.split(", ")
    correct_address_list: list[str] = []

    # Check if the first element is a PO box
    if "PO Box" in address_elements[0]:
        correct_address_list.append(address_elements.pop(0).split(" ")[2])
    else:
        correct_address_list.append("")

    # Check if the second element is of the form "number street"
    if address_elements[0].split(" ")[0].isdigit():
        st_number, st_name = address_elements.pop(0).split(" ", 1)
        correct_address_list.extend([st_name, st_number])
    else:
        correct_address_list.extend(["", ""])

    # Check if the third element is the same as the city
    while len(address_elements) > 0 and address_elements[0] != city:
        address_elements.pop(0)
    if len(address_elements) == 0:
        print(f"City '{city}' not found in address '{address}'\nCurrent elements: {address_elements}\nCorrect address list: {correct_address_list}")
        return None
    else:
        correct_address_list.append(address_elements.pop(0))

    # Check if the fourth element is of the form "state_code zip"
    while len(address_elements) > 0 and address_elements[0].split(" ")[0] != us_state_to_abbrev[state]:
        address_elements.pop(0)
    if len(address_elements) == 0:
        print(f"State '{state}' not found in address '{address}'\nCurrent elements: {address_elements}\nCorrect address list: {correct_address_list}")
        return None
    else:
        correct_address_list.append(address_elements.pop(0).split(" ")[1])

    # Add county at the end
    correct_address_list.append(county)

    return ",".join([ele.strip() if ele != '' else ' ' for ele in correct_address_list])
dan['address'] = dan.apply(lambda x: fix_address_format(x['state'], x['county'], x['city'], x['address']), axis=1)

# Add missing columns
dan['country'] = "USA"
dan['latitude'] = None
dan['longitude'] = None

# Define the desired order of columns
desired_columns = ['name', 'country', 'state', 'address', 'latitude', 'longitude', 'info']

# Reorganize the columns
dan = dan.reindex(columns=desired_columns)

# Rename "state" to "city"
dan = dan.rename(columns={'state': 'city'})

# Remove rows with empty address
dan = dan[dan['address'].notna()]

# Export the processed dataframe to a new CSV file
dan.to_csv('data/autism_treatment_centers_autism_now_processed.csv', index=False)

# Merge with the manually processed autism_center_b.csv file

# Read the CSV file
final_d = pd.read_csv('data/autism_center_b.csv')

# reorder the columns "city"-"country" to "country"-"city"
final_d = final_d[['name', 'country', 'city', 'address', 'latitude', 'longitude', 'info', 'free_quote_link']]

merged_df = pd.concat([final_d, dan], ignore_index=True)
merged_df.to_csv('data/autism_center.csv', index=False)


