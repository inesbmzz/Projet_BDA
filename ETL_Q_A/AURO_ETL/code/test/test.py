import pandas as pd
import unittest
import os
import json

class TestConcatenation(unittest.TestCase):
    def test_length(self):
        print("Running test_length: Verifying the total length of concatenated DataFrame.")
        # Load individual CSV files
        df1 = pd.read_csv('data/transform_in/childmind_extracted_data.csv', usecols=['Question', 'Answer'])
        df2 = pd.read_csv('data/transform_in/medscape_extracted_data.csv', usecols=['Question', 'Answer'])
        df3 = pd.read_csv('data/transform_in/parent_guid_extracted_data.csv', usecols=['Question', 'Answer'])
        
        # Concatenate the dataframes vertically
        concatenated_df = pd.concat([df1, df2, df3])

        # Calculate the expected total length
        total_length_expected = len(df1) + len(df2) + len(df3)

        # Check if total length matches
        self.assertEqual(len(concatenated_df), total_length_expected)

    def test_column_exists(self):
        print("Running test_column_exists: Verifying if 'Source' column exists in the concatenated DataFrame.")
        # Load the concatenated DataFrame
        concatenated_df = pd.read_csv('data/transform_in/all_extracted_data.csv')

        # Check if 'Source' column exists
        self.assertTrue('Source' in concatenated_df.columns)

    def test_json_length(self):
        print("Running test_json_length: Verifying if length of JSON file matches the length of concatenated DataFrame.")
        # Load the concatenated DataFrame
        concatenated_df = pd.read_csv('data/transform_in/all_extracted_data.csv')

        # Load the JSON file
        with open('data.json', 'r') as f:
            json_data = json.load(f)

        # Check if length of JSON data matches the length of concatenated DataFrame
        self.assertEqual(len(json_data), len(concatenated_df))

if __name__ == '__main__':
    unittest.main()
