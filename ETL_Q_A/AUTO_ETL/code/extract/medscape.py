import PyPDF2
import csv
import re
import pandas as pd


print('                start extract medscape')



content_array = [
    "Practice Essentials",
    "Signs and symptoms",
    "Diagnosis",
    "Management",
    "Background",
    "Motion anomalies",
    "Causes",
    "Diagnosis",
    "Treatment",
    "Neural anomalies",
    "Gamma-amino butyric acid (GABA)",
    "Glutathione (GSH)",
    "N-acetylaspartate (NAA)",
    "Metabolic anomalies",
    "Mitochondrial dysfunction",
    "Neural inflammation",
    "Etiology",
    "Obstetric complications",
    "Infection",
    "Familial and genetic factors",
    "Toxic exposure",
    "Parental age",
    "Vaccination",
    "Epidemiology",
    "Occurrence in the United States",
    "International occurrence",
    "Sex-related demographics",
    "Prognosis",
    "Comorbid disorders",
    "Patient Education",
    "Obtaining informed consent",
    "Additional resources",
    "History",
    "Developmental regression",
    "Protodeclarative pointing",
    "Environmental stimuli",
    "Social interactions",
    "High pain threshold",
    "Language",
    "Play",
    "Response to febrile illnesses",
    "Autism Screening Checklist",
    "Screening",
    "Body movement",
    "Head and hand features",
    "Movement assessment",
    "Assessing stereotypies",
    "Self-injurious behaviors",
    "Physical abuse",
    "Sexual abuse",
    "Examination of siblings",
    "Diagnostic Considerations",
    "Diagnostic error and clinician experience",
    "Screening tests",
    "Cultural considerations",
    "Other disorders",
    "Age of onset",
    "Differential Diagnoses",
    "Approach Considerations",
    "Metabolic studies",
    "Neuroimaging",
    "Electroencephalography",
    "Psychophysiologic assessment",
    "Polysomnography",
    "Genetic Testing",
    "MRI",
    "Diffusion tensor imaging",
    "Computed tomography",
    "Positron emission tomography scanning",
    "SPECT (single-photon emission CT) scanning",
    "Electroencephalography",
    "Approach Considerations",
    "Inpatient Psychiatric Care",
    "Special Education",
    "Speech, Behavioral, Occupational, and Physical Therapies",
    "Cognitive behavior therapy (CBT)",
    "Family therapy",
    "Mind-body exercise",
    "Diet",
    "Pharmacologic Treatment",
    "SSRIs",
    "Adverse effects and treatment efficacy",
    "Experimental Approaches",
    "Transcranial magnetic stimulation",
    "Secretin therapy",
    "Hyperbaric oxygen therapy",
    "Intranasal oxytocin",
    "Specialist Resources",
    "Consultations",
    "Guidelines Summary",
    "Medication Summary",
    "Class Summary",
    "Risperidone (Risperdal, Risperdal Consta, Risperdal M-Tab)",
    "Aripiprazole (Abilify, Abilify MyCite)",
    "Ziprasidone (Geodon)",
    "Class Summary",
    "Fluoxetine (Prozac)",
    "Citalopram (Celexa)",
    "Escitalopram (Lexapro)",
    "Class Summary",
    "Methylphenidate (Ritalin, Quillivant XR, Ritalin LA, Concerta)",
    "Class Summary",
    "Clonidine (Catapres, Catapres-TTS, Kapvay)",
    "Guanfacine (Intuniv)"
]

# Open the PDF file
with open('data/source/medscape_content.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    # Define the range of pages to extract questions from
    start_page = 1
    end_page = 30

    extracted_text = ""
    
    # Loop through the specified pages
    for page_num in range(start_page - 1, end_page):
        page = reader.pages[page_num]
        text = page.extract_text()
        
        # Remove time, links, and page numbers using regular expressions
        text = re.sub(r'\d+/\d+/\d+, \d+:\d+ [AP]M', '', text)  # Remove time
        text = re.sub(r'https?://\S+', '', text)  # Remove links
        text = re.sub(r'\d+/\d+', '', text)  # Remove page numbers
        
        extracted_text += text


# Write the extracted content to CSV
with open('data/extract_out/medscape/answer/extracted_text.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Keyword", "Answer"])

    # Iterate through each word in the array
    for word in content_array:
        # Find the index of the word in the extracted text
        start_index = extracted_text.find(word)
        if start_index != -1:
            # Find the next index of the next word in the array
            if content_array.index(word)+1 != len(content_array):
                next_word_index = extracted_text.find(content_array[content_array.index(word) + 1])
            else:
                next_word_index = -1
            # If next word exists, slice text between current and next word
            if next_word_index != -1:
                answer = extracted_text[start_index:next_word_index]
            # If next word doesn't exist, slice text from current word to end of text
            else:
                answer = extracted_text[start_index:]
            writer.writerow([word, answer.strip().replace("\n","")])





# Open the PDF file
with open('data/source/medscape_content.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    # Define the range of pages to extract questions from
    start_page = 30
    end_page = 33

    extracted_text = ""
    
    # Loop through the specified pages
    for page_num in range(start_page - 1, end_page):
        page = reader.pages[page_num]
        text = page.extract_text()
        extracted_text += text



# Write the extracted text to a .txt file
with open('data/extract_out/medscape/question/extracted_text.txt', 'w') as txt_file:
    txt_file.write(extracted_text)


# Read the extracted text from the .txt file
with open('data/extract_out/medscape/question/extracted_text.txt', 'r') as txt_file:
    lines = txt_file.read().split('\n')


# Write the extracted text to a CSV file with header
with open('data/extract_out/medscape/question/extracted_text.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the header row
    writer.writerow(['Question'])
    # Write each line of text as a row
    for line in lines:
        writer.writerow([line])

questions_df = pd.read_csv("data/extract_out/medscape/question/extracted_text.csv")
answers_df = pd.read_csv("data/extract_out/medscape/answer/extracted_text.csv")


questions_df['index'] = range(1, len(questions_df) + 1)
answers_df['index'] = range(1, len(answers_df) + 1)



# Merge the DataFrames based on the index column
merged_df = pd.merge(questions_df, answers_df, on='index')

# Drop the index column
merged_df.drop(columns=['index'], inplace=True)

# Save the merged DataFrame to a new CSV file
merged_df.to_csv("data/extract_out/medscape_extracted_data.csv", index=False)


print('                end extract medscape')
