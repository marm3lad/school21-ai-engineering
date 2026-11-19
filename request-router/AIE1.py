import json
import csv
import argparse
import sys

# Реальный функции для моего проекта для чтения JSOM и CSV файлов
def read_json(path):
    with open(path, 'r', encoding="utf-8") as f:
        содержимое = json.load(f)
    return содержимое

def read_csv(path):
    with open(path, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        содержимое = list(reader)
    return содержимое

def read_requests(path):
    if path.endswith('.csv'):
        результат = read_csv(path)
        return результат
    elif path.endswith('.json'):
        результат = read_json(path)
        return результат
    else:
        return "Не подходящий формат"

def normalize_record(record):
    id_raw = record.get("id")
    text_raw = record.get("text")

    # Проверяем ДО преобразования в строку
    if not id_raw or not text_raw:
        raise ValueError("Запись должна иметь id и text")

    id = str(id_raw).strip().lower().replace("ё", "е")
    text = str(text_raw).strip().lower().replace("ё", "е")
    return {"id": id, "text": text}

def determine_priority(text, category):
    if "срочно" in text or "критично" in text or "недоступен всем" in text:
        return "high"
    elif category == "access" or category == "bug":
        return "medium"
    else:
        return "low"

def determine_category(text):
    if "войти" in text or "пароль" in text or "нет доступа" in text:
        return "access"
    elif "оплата" in text or "счет" in text or "тариф" in text or "спис" in text:
        return "billing"
    elif "ошибка" in text or "не работает" in text or "падает" in text or "недоступен" in text:
        return "bug"
    else:
        return "other"

def route_request(record):
    очищенная = normalize_record(record)
    категория = determine_category(очищенная["text"])
    приоритет = determine_priority(очищенная["text"], категория)
    return {"id": очищенная["id"], "category": категория, "priority": приоритет}

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True, help="Путь к входному файлу")
    parser.add_argument("--output", required=True, help="Путь к выходному файлу")

    args = parser.parse_args()

    try:
        результат = read_requests(args.input)

        обработанные_записи = []
        for одна_запись in результат:
            маршрутизированная = route_request(одна_запись)
            обработанные_записи.append(маршрутизированная)
        with open(args.output, 'w', encoding="utf-8") as f:
            json.dump(обработанные_записи, f, ensure_ascii=False, indent=2)
        print("Успешно обработано")
        sys.exit(0)

    except FileNotFoundError:
        print("Ошибка: файл не найден")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Ошибка: JSON поврежден")
        sys.exit(1)
    except ValueError:
        print("Ошибка: в записи отсутствует или пусто поле id либо text")
        sys.exit(1)

if __name__ == '__main__':
    main()