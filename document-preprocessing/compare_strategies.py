import os, json

from text_cleaner import clean_text
from chunking import chunk_document, tokenize_by_words, tokenize_by_sentences

DOCUMENT_PATH = "data/long_document.txt"
QUESTIONS = [
    {"question": "За сколько минут нужно ответить на заявку с высоким приоритетом?",
     "answer": "на заявку с высоким приоритетом оператор должен ответить в течение 15 минут"},
    {"question": "Когда заявку передают во вторую линию и что сделать перед передачей?",
     "answer": "если оператор первой линии не может решить проблему за 30 минут работы, заявка передаётся во вторую линию. перед передачей обязательно опишите в карточке, что уже было проверено, какие шаги предпринимались и что ответил клиент."},
    {"question": "Какие данные нужны для проверки личности клиента?",
     "answer": "для проверки личности достаточно последних четырёх цифр номера договора и даты рождения владельца."},
    {"question": "Как часто нужно менять пароль?",
     "answer": "пароль от рабочей учётной записи нужно менять каждые 90 дней"},
]

def load_document(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def count_broken(chunks):
    count = 0
    for chunk in chunks:
        if not(chunk.endswith((".", "!", "?"))):
            count += 1
    return count

def count_found_answers(chunks, questions):
    count = 0
    for question in questions:
        for chunk in chunks:
            if question["answer"] in chunk:
                count += 1
                break
    return count

def calculate_metrics(chunks):
    count_chunks = len(chunks)
    avg_symbol = 0
    for chunk in chunks:
        avg_symbol += len(chunk)
    avg_symbol /= count_chunks

    avg_word = 0
    for chunk in chunks:
        avg_word += len(tokenize_by_words(chunk))
    avg_word /= count_chunks

    return {
        "Количество чанков": count_chunks,
        "Средний размер в символах": round(avg_symbol, 1),
        "Средний размер в словах": round(avg_word, 1),
        "Обрываются посреди предложения": count_broken(chunks),
        "Ответов целиком в одном чанке": count_found_answers(chunks, QUESTIONS),
    }

def save_chunks(chunks, path, tokenizer):
    all_chunks = []
    for chunk_index, chunk in enumerate(chunks):
        token_count = len(tokenizer(chunk))
        record = {"document_id": 1, "chunk_index": chunk_index, "text": chunk, "token_count": token_count}
        all_chunks.append(record)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=4)

def main():
    raw_text = load_document(DOCUMENT_PATH)
    cleared_text = clean_text(raw_text)

    chunks_A = chunk_document(cleared_text, tokenizer=tokenize_by_sentences, chunk_size=3, overlap_size=1)
    chunks_B = chunk_document(cleared_text, tokenizer=tokenize_by_words, chunk_size=50, overlap_size=10)
    metrics_a = calculate_metrics(chunks_A)
    metrics_b = calculate_metrics(chunks_B)
    print(f"{'Метрика':<30}|{'A':>6}|{'B':>6}|")
    print(f"{'Количество чанков':<30}|{metrics_a['Количество чанков']:>6}|{metrics_b['Количество чанков']:>6}|")
    print(f"{'Средний размер в символах':<30}|{metrics_a['Средний размер в символах']:>6}|{metrics_b['Средний размер в символах']:>6}|")
    print(f"{'Средний размер в словах':<30}|{metrics_a['Средний размер в словах']:>6}|{metrics_b['Средний размер в словах']:>6}|")
    print(f"{'Обрываются посреди предложения':<30}|{metrics_a['Обрываются посреди предложения']:>6}|{metrics_b['Обрываются посреди предложения']:>6}|")
    print(f"{'Ответов целиком в одном чанке':<30}|{metrics_a['Ответов целиком в одном чанке']:>6}|{metrics_b['Ответов целиком в одном чанке']:>6}|")
    save_chunks(chunks_A, "results/strategy_A.json", tokenizer=tokenize_by_sentences)
    save_chunks(chunks_B, "results/strategy_B.json", tokenizer=tokenize_by_words)

if __name__ == "__main__":
    main()