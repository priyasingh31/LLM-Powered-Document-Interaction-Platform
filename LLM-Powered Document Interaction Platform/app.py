from langchain_community.llms.ollama import Ollama  # Correct import
import pdfplumber
import os
import docx
import pandas as pd
import streamlit as st

# Instantiate the LLM model
olla = Ollama(base_url="http://localhost:11434", model="llama3.1")

UPLOAD_DIR = "uploaded_files"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def save_file(uploaded_file):
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def get_file_extension(file_name):
    return os.path.splitext(file_name)[1].lower()

def read_pdf_content(pdf_file):
    content = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            content += text + "\n"
    return content

def read_doc_content(doc_file):
    content = ""
    doc = docx.Document(doc_file)
    for paragraph in doc.paragraphs:
        content += paragraph.text + "\n"
    return content

def read_txt_content(txt_file):
    with open(txt_file, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def read_code_content(code_file):
    with open(code_file, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def read_csv_and_xls_content(file_path):
    file_extension = get_file_extension(file_path)
    if file_extension == ".csv":
        df = pd.read_csv(file_path)
        return df.to_string()
    elif file_extension in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path)
        return df.to_string()

def process_file(file):
    # Save the file and get the file path
    file_path = save_file(file)
    # Get the file extension
    file_extension = get_file_extension(file.name)
    
    if file_extension == ".pdf":
        content = read_pdf_content(file_path)
    elif file_extension in [".doc", ".docx"]:
        content = read_doc_content(file_path)
    elif file_extension == ".txt":
        content = read_txt_content(file_path)
    elif file_extension in [".py", ".js", ".java", ".cpp", ".c", ".html", ".css", ".xml", ".sh", ".rb", ".sql"]:
        content = read_code_content(file_path)
    elif file_extension in [".csv", ".xls", ".xlsx"]:
        content = read_csv_and_xls_content(file_path)
    else:
        raise ValueError("Unsupported file type. Please provide a PDF, DOC, DOCX, TXT, code, or CSV/XLS file.")
    
    return content

def answer_query(content, query):
    prompt = content + "\n" + query
    response = olla(prompt)
    return response

def save_response(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Response saved to {file_path}")

# Main function
def main():
    st.title("Multi-File LLM Interaction Platform")

    # File uploader allowing multiple files
    uploaded_files = st.file_uploader("Upload multiple files", accept_multiple_files=True)

    # Text input for the prompt
    query = st.text_input("Input your prompt", placeholder="Enter your query here...")

    # Process files and generate a response
    if st.button("Generate Response") and uploaded_files and query:
        all_content = ""
        for uploaded_file in uploaded_files:
            content = process_file(uploaded_file)
            all_content += content

        response = answer_query(all_content, query)
        st.write(response)

if __name__ == "__main__":
    main()
