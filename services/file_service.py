import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_FILES_DIR = os.path.join(BASE_DIR, "test_files")


def get_local_files():

    files = []

    for filename in os.listdir(TEST_FILES_DIR):

        file_path = os.path.join(TEST_FILES_DIR, filename)

        if os.path.isfile(file_path):
            files.append(filename)

    return files

import pymupdf


def extract_pdf_text(file_path):

    document = pymupdf.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text

def search_files(query):

    query = query.lower()

    results = []

    for filename in get_local_files():

        if not filename.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(TEST_FILES_DIR, filename)

        text = extract_pdf_text(file_path)

        text_lower = text.lower()

        position = text_lower.find(query)

        if position != -1:

            start = max(0, position - 200)
            end = min(len(text), position + len(query) + 300)

            snippet = text[start:end].strip()

            results.append({
                "filename": filename,
                "snippet": snippet
            })

    return results

if __name__ == "__main__":

    query = "class diagram"

    results = search_files(query)

    print("Search results for:", query)

    for result in results:

        print("\nFile:", result["filename"])
        print("Relevant text:")
        print(result["snippet"])