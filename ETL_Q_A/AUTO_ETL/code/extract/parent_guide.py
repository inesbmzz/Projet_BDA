import fitz  # PyMuPDF
import csv
import re


print('                start extract parent guide')


def read_pdf_pages(pdf_path, start_page, end_page):
    text = ''
    with fitz.open(pdf_path) as pdf_document:
        for page_number in range(start_page - 1, min(end_page, pdf_document.page_count)):
            page = pdf_document[page_number]
            text += page.get_text()

    return text

# Specify your PDF file path and page range
pdf_path = 'data/source/Book.pdf'
start_page = 13
end_page = 15

# Read and print the content of the specified pages
result = read_pdf_pages(pdf_path, start_page, end_page)


def extract_qa(text):
    # Split the text into questions and answers based on the 'Q:' pattern
    qa_pairs = re.split(r'\bQ:', text)[1:]
    
    
    # Extract questions and answers
    questions = []
    answers = []

    for qa in qa_pairs:
        parts = re.split(r'\?\s*\n', qa)
        
        # Check if splitting based on "?\s*\n" pattern resulted in more than one part
        if len(parts) > 1:
            question, answer = parts[0], parts[1]
        else:
            # If not, try splitting based on period (.)
            parts = re.split(r'\.\s*\n', qa)
            question, answer = parts[0], parts[1] if len(parts) > 1 else ''

        questions.append(question.strip().replace(',', '').replace('\n',''))
        answers.append(answer.strip().replace(',', '').replace('\n',''))
    
    return zip(questions, answers)

def save_to_csv(qa_pairs, csv_filename):
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(['Question', 'Answer'])

        # Write data
        writer.writerows(qa_pairs)


# Extract questions and answers
qa_pairs = extract_qa(result)

# Save to CSV file
csv_filename = 'data/extract_out/parent_guid_extracted_data.csv'
save_to_csv(qa_pairs, csv_filename)



print('                end extract parent guide')
