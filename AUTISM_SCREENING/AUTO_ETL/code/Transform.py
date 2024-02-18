import pandas as pd


# Read data from CSV files
print("Reading data from CSV files...")
df1 = pd.read_csv('data/Autism-Adolescent-Data.csv', na_values=['?'])
df2 = pd.read_csv('data/Autism-Adult_Data.csv', na_values=['?'])
df3 = pd.read_csv('data/Autism-Child-Data.csv', na_values=['?'])

# Concatenating df1, df2, and df3 into a single DataFrame
print("Concatenating dataframes...")
data = pd.concat([df1, df2, df3], ignore_index=True)

# Dropping specified columns
print("Dropping specified columns...")
columns_to_drop = ['Unnamed: 0', 'contry_of_res', 'used_app_before', 'age_desc']
data = data.drop(columns=columns_to_drop)

# Dropping rows with null values in specified columns
print("Dropping rows with null values...")
data = data.dropna(subset=['age', 'gender', 'ethnicity', 'jundice', 'austim', 'result', 'relation'])

# Dropping duplicate rows
print("Dropping duplicate rows...")
data = data.drop_duplicates()


# Convert 'age' column to integer
print("Converting 'age' column to integer...")
data['age'] = data['age'].astype(int)


# Remove rows where age is greater than 150
print("Removing rows where age is greater than 150...")
data = data[data['age'] <= 150]


# Save the transformed data to CSV
print("Saving transformed data to CSV...")
data.to_csv("Autism_test_clean.csv", index=False, header=False)


