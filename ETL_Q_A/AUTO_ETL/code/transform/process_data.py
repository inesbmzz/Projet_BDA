import re
import pandas as pd


# Load the three CSV files into dataframes
df1 = pd.read_csv('data/transform_in/childmind_extracted_data.csv', usecols=['Question', 'Answer'])
df2 = pd.read_csv('data/transform_in/medscape_extracted_data.csv', usecols=['Question', 'Answer'])
df3 = pd.read_csv('data/transform_in/parent_guid_extracted_data.csv', usecols=['Question', 'Answer'])


# Add a 'Source' column to each dataframe 
df1['Source'] = 'childmind'
df2['Source'] = 'medscape'
df3['Source'] = 'parent_guid'

# Concatenate the dataframes vertically
concatenated_df = pd.concat([df1, df2, df3])


# Reset the index of the concatenated dataframe
concatenated_df.reset_index(drop=True, inplace=True)


concatenated_df.to_csv('data/transform_in/all_extracted_data.csv')



# Load the three CSV files into dataframes
df = pd.read_csv('data/transform_in/all_extracted_data.csv')

# Remove the 'Unnamed: 0' column
df.drop(columns=['Unnamed: 0'], inplace=True)

# Define a function to replace the patterns in the 'Answer' column
def replace_patterns(answer):
    # Remove patterns like [1], [4,3], [2, 4,3]
    pattern = r'\[\d+(?:,\s*\d+)*\]'
    answer = re.sub(pattern, '', answer)
    
    # Remove "See the image " 
    answer = re.sub(r'See the image .*?\.', '.', answer)

    answer = re.sub(r'read more .*?\.', '.', answer)
    
    return answer

# Apply the function to the 'Answer' column
df['Answer'] = df['Answer'].apply(replace_patterns)


df.to_csv('data/transform_in/Clean_data.csv')

# Convert DataFrame to JSON
import json

json_data = df.to_json(orient='records')

json_data = json.loads(json_data)


from json_exemples import *


json_data[104] = Alpha_2_adrenergic_agonists
json_data[105] = Stimulants
json_data[106] = SSRI_Antidepressants
json_data[107] = second_Generation_Antipsychotics

json_data[0] = ASD
json_data[2] = Autism_Diagnosed
json_data[3] = Autism_Diagnoses_Delayed



# Specify the file path where you want to save the JSON data
json_file_path = 'data.json'

# Write JSON data to the file
with open(json_file_path, 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

print(f"JSON data has been saved to {json_file_path}")