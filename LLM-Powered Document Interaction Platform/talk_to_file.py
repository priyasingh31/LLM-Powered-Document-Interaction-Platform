import os
import PyPDF2
import pandas as pd
from docx import Document
from transformers import pipeline

# Initialize the language model pipeline
llm_pipeline = pipeline('text-generation', model='distilgpt2')

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extract_text()
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_txt(file_path):
    with open(file_path, "r") as file:
        text = file.read()
    return text

def extract_data_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df

def extract_data_from_xlsx(file_path):
    df = pd.read_excel(file_path)
    return df

def read_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    elif ext == '.txt':
        return extract_text_from_txt(file_path)
    elif ext == '.csv':
        return extract_data_from_csv(file_path)
    elif ext in ['.xls', '.xlsx']:
        return extract_data_from_xlsx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def process_files(file_paths):
    contents = {}
    for file_path in file_paths:
        try:
            contents[file_path] = read_file(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    return contents

def analyze_relationships(dataframes):
    relationships = {}
    for name, df in dataframes.items():
        relationships[name] = {}
        columns = df.columns
        for col in columns:
            relationships[name][col] = {}
            # Check for missing values
            relationships[name][col]['missing_values'] = df[col].isnull().sum()
            # Basic statistics
            relationships[name][col]['mean'] = df[col].mean()
            relationships[name][col]['std_dev'] = df[col].std()
    return relationships

def ask_question(content_dict, question):
    combined_text = "\n".join([text for text in content_dict.values() if isinstance(text, str)])
    response = llm_pipeline(f"{combined_text}\n\nQuestion: {question}", max_length=500)
    return response[0]['generated_text']

def main():
    files = input("Enter the paths of the files (comma-separated): ").split(',')
    files = [file.strip() for file in files]
    
    content_dict = process_files(files)
    
    # Separate text files and dataframes
    text_contents = {k: v for k, v in content_dict.items() if isinstance(v, str)}
    dataframes = {k: v for k, v in content_dict.items() if isinstance(v, pd.DataFrame)}
    
    # Analyze relationships between dataframes
    relationships = analyze_relationships(dataframes)
    
    # Print relationships
    print("\nData Relationships:")
    for name, cols in relationships.items():
        print(f"\nFile: {name}")
        for col, stats in cols.items():
            print(f"Column: {col}")
            print(f"  Missing Values: {stats['missing_values']}")
            print(f"  Mean: {stats['mean']}")
            print(f"  Standard Deviation: {stats['std_dev']}")
    
    question = input("\nEnter your question related to the files: ")
    answer = ask_question(text_contents, question)
    
    print("\nAnswer:")
    print(answer)

if __name__ == "__main__":
    main()
