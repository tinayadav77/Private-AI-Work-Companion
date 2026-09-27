from sentence_transformers import SentenceTransformer
import numpy as np
import os

from services.file_service import get_local_files, extract_pdf_text


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

model = SentenceTransformer("all-MiniLM-L6-v2")


def create_chunks(text, chunk_size=800):
    chunks = []

    for i in range(0, len(text), chunk_size):

        chunk = text[i:i + chunk_size].strip()

        if chunk:
            chunks.append(chunk)

    return chunks


def search_documents(query):

    all_chunks = []
    chunk_files = []

    query_lower = query.lower()

    for filename in get_local_files():

        if not filename.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(
            BASE_DIR,
            "test_files",
            filename
        )

        # -----------------------------
        # 1. Filename matching
        # -----------------------------

        filename_lower = filename.lower()

        filename_words = (
            filename_lower
            .replace(".pdf", "")
            .replace("_", " ")
            .replace("-", " ")
        )

        filename_match = 0.0

        query_words = query_lower.split()

        for word in query_words:
            if len(word) > 2 and word in filename_words:
                filename_match += 1

        if query_words:
            filename_match = filename_match / len(query_words)

        # -----------------------------
        # 2. Semantic content matching
        # -----------------------------

        text = extract_pdf_text(file_path)

        chunks = create_chunks(text)

        for chunk in chunks:

            all_chunks.append(chunk)
            chunk_files.append(filename)

        # If the PDF has no readable text,
        # filename matching can still find it.
        if not chunks:
            all_chunks.append("")
            chunk_files.append(filename)

    if not all_chunks:
        return []

    # -----------------------------
    # Semantic embeddings
    # -----------------------------

    document_embeddings = model.encode(all_chunks)

    query_embedding = model.encode(query)

    similarities = np.dot(
        document_embeddings,
        query_embedding
    ) / (
        np.linalg.norm(document_embeddings, axis=1)
        * np.linalg.norm(query_embedding)
    )

    # -----------------------------
    # Best score per file
    # -----------------------------

    best_files = {}

    for index, similarity in enumerate(similarities):

        filename = chunk_files[index]

        semantic_score = float(similarity)

        if filename not in best_files:

            best_files[filename] = {
                "semantic": semantic_score,
                "snippet": all_chunks[index]
            }

        elif semantic_score > best_files[filename]["semantic"]:

            best_files[filename] = {
                "semantic": semantic_score,
                "snippet": all_chunks[index]
            }

    # -----------------------------
    # Combine filename + semantic score
    # -----------------------------

    results = []

    for filename, data in best_files.items():

        filename_lower = filename.lower()

        filename_words = (
            filename_lower
            .replace(".pdf", "")
            .replace("_", " ")
            .replace("-", " ")
        )

        filename_score = 0.0

        for word in query_words:
            if len(word) > 2 and word in filename_words:
                filename_score += 1

        if query_words:
            filename_score = filename_score / len(query_words)

        semantic_score = data["semantic"]

        # Filename matches are useful, but
        # semantic meaning still carries more weight.
        combined_score = (
            semantic_score * 0.7
            + filename_score * 0.3
        )

        results.append({
            "filename": filename,
            "similarity": combined_score,
            "snippet": data["snippet"]
        })

    # -----------------------------
    # Rank results
    # -----------------------------

    results.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    # Return top 5
    final_results = []

    for result in results[:5]:

        # Ignore genuinely unrelated files
        if result["similarity"] < 0.25:
            continue

        final_results.append(result)

    return final_results


# Sort files by their best relevance score
    sorted_files = sorted(
        best_files.items(),
        key=lambda item: item[1]["similarity"],
        reverse=True
)


# Return only reasonably relevant files
    results = []

    for filename, data in sorted_files[:5]:

        if data["similarity"] < 0.40:
            continue

        results.append({
        "filename": filename,
        "similarity": data["similarity"],
        "snippet": data["snippet"]
    })

    return results


if __name__ == "__main__":

    query = "class diagram"

    results = search_documents(query)

    print("\nSearch:", query)

    for result in results:

        print("\n-------------------------")
        print("File:", result["filename"])
        print("Similarity:", result["similarity"])
        print("Snippet:")
        print(result["snippet"][:500])