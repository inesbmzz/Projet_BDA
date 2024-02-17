import pandas as pd

# Read the final CSV file
data = pd.read_csv("Autism_test_clean.csv")

# Verify that specified columns are removed
columns_to_drop = ['Unnamed: 0', 'contry_of_res', 'used_app_before', 'age_desc']
removed_columns = set(columns_to_drop).intersection(set(data.columns))
if removed_columns:
    print("❌ Columns that were not removed:")
    for column in removed_columns:
        print(f"   - {column}")
else:
    print("✅ All specified columns were removed successfully.")

# Check for duplicate rows
if data.duplicated().any():
    print("❌ Duplicate rows exist.")
else:
    print("✅ No duplicate rows found.")

# Check for null values
null_values = data.isnull().sum()
if null_values.sum() > 0:
    print("❌ Null values exist in the following columns:")
    for column, count in null_values.items():
        if count > 0:
            print(f"   - {column}: {count} null values")
else:
    print("✅ No null values found.")


# Check if all tests passed
if removed_columns or data.duplicated().any() or null_values.sum() > 0:
    print("\n❌ Test failed.")
else:
    print("\n✅ Tests passed.")
