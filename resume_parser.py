print("Loaded resume_parser from:", __file__)

import PyPDF2
import docx


def extract_text(uploaded_file):
    file_name = uploaded_file.name.lower()

    # -----------------------------
    # Read PDF
    # -----------------------------
    if file_name.endswith(".pdf"):

        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        text = ""

        for page in pdf_reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

        return text

    # -----------------------------
    # Read DOCX
    # -----------------------------
    elif file_name.endswith(".docx"):

        document = docx.Document(uploaded_file)

        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    # -----------------------------
    # Read TXT
    # -----------------------------
    elif file_name.endswith(".txt"):

        return uploaded_file.read().decode("utf-8")

    # -----------------------------
    # Unsupported File
    # -----------------------------
    else:

        return ""