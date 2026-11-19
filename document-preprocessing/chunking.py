import re
import json

CHUNK_SIZE = 3
OVERLAP_SIZE = 1

def tokenize_by_words(text):
    tokens = text.split()
    return tokens

def tokenize_by_sentences(text):
    parts = re.split(r"(?<=[.?!])\s+", text)
    sentences = []
    for part in parts:
        if re.search(r"[а-яёА-ЯЁa-zA-Z]", part):
            sentences.append(part)
    return sentences

TOKENIZER = tokenize_by_sentences # в предложениях

def chunk_fixed_size(tokens, chunk_size, overlap_size):
    if overlap_size >= chunk_size or chunk_size <= 0 or overlap_size < 0:
        raise ValueError("шаг не может быть нулевым, или быть отрицательным")
    step = chunk_size - overlap_size
    chunks = []
    start = 0
    while start < len(tokens):
        chunk = tokens[start: start + chunk_size]
        chunks.append(chunk)
        if start + chunk_size >= len(tokens):
            break
        start += step
    return chunks

def chunk_document(text, tokenizer=TOKENIZER, chunk_size=CHUNK_SIZE, overlap_size=OVERLAP_SIZE):
    tokens = tokenizer(text)
    chunks = chunk_fixed_size(tokens, chunk_size, overlap_size)

    chunks_str = []
    for chunk in chunks:
        line = " ".join(chunk)
        chunks_str.append(line)
    return chunks_str

def main():
    with open("data/cleaned_documents.txt",  "r", encoding="utf-8") as f:
        text = f.read()
    documents = re.split(r"\n---\n", text)

    all_chunks = []
    for document_id, document in enumerate(documents, start=1):
        chunks = chunk_document(document)
        for chunk_index, chunk in enumerate(chunks):
            token_count = len(TOKENIZER(chunk))
            record = {"document_id": document_id, "chunk_index": chunk_index, "text": chunk, "token_count": token_count}
            all_chunks.append(record)

    with open("data/chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()