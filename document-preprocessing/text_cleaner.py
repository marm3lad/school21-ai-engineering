import re

def normalize_whitespace(text):
    normalize_words = text.split()
    return ' '.join(normalize_words)

def remove_special_characters(text, keep_punctuation=True):
    if keep_punctuation:
        cleared_text = re.sub(r"[^0-9a-zA-Zа-яА-ЯёЁ.,?! -]", " ", text)
    else:
        cleared_text = re.sub(r"[^0-9a-zA-Zа-яА-ЯёЁ ]", " ", text)
    return normalize_whitespace(cleared_text)

def normalize_case(text, lower=True):
    if lower:
        case = text.lower()
    else:
        case = text
    return case


def clean_text(text, **kwargs):
    normalize_words = normalize_whitespace(text)
    cleared_text = remove_special_characters(normalize_words, kwargs.get("keep_punctuation", True))
    case = normalize_case(cleared_text, kwargs.get("lower", True))
    return case

def main():
    with open("data/sample_documents.txt", "r", encoding="utf-8") as f:
        text = f.read()
    parts = re.split(r"--- DOCUMENT_\d+:.*", text)
    documents = []
    for part in parts:
        cleaned = part.strip()
        if cleaned:
            cleaned = clean_text(cleaned)
            documents.append(cleaned)
    with open("data/cleaned_documents.txt", "w", encoding="utf-8") as f:
        f.write("\n---\n".join(documents))

if __name__ == '__main__':
    main()