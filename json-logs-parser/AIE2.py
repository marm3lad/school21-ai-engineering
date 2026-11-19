import json
import sys
import os
TOKEN_THRESHOLD = 1000

def load_logs(path):
    items = []
    with open(path, 'r', encoding="utf-8") as f:
        for number, line in enumerate(f, start=1):
            line = line.strip()
            if line == "":
                continue
            else:
                new_line = json.loads(line)
                if not isinstance(new_line, dict):
                    print('Предупреждение: строка', number, 'не является словарём, пропущена', file=sys.stderr)
                    continue
                items.append(new_line)
        if not items:
            print("Нет ни одной валидной записи", file=sys.stderr)
    return items

def filter_logs(logs, threshold):
    filtered_logs = []
    for log in logs:
        if log.get("tokens_used") is None:
            continue
        elif not is_number(log.get("tokens_used")):
            print("Предупреждение: tokens_used не число,", log.get("timestamp"), "пропущена", file=sys.stderr)
            continue
        elif log.get("tokens_used") > threshold:
            filtered_logs.append(log)
    return filtered_logs

def save_filtered(logs):
    with open ('results/filtered_logs.json', 'w', encoding="utf-8") as f:
        for log in logs:
            f.write(json.dumps(log, ensure_ascii=False))
            f.write("\n")

def save_report(report):
    with open("results/report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

def calculate_metrics(filtered_logs,total_entries, threshold):
    total_tokens = 0
    latencies = []
    quantity_errors = 0

    for filtered_log in filtered_logs:
        total_tokens += filtered_log.get("tokens_used")
        if filtered_log.get("error"):
            quantity_errors += 1
        if filtered_log.get("latency_ms") is None:
            continue
        elif is_number(filtered_log.get("latency_ms")):
            latencies.append(filtered_log.get("latency_ms"))
        else:
            print("Предупреждение: latency_ms не число,", filtered_log.get("timestamp"), "пропущена", file=sys.stderr)

    if latencies:
        average = sum(latencies) / len(latencies)
        average = round(average, 2)
    else:
        average = None

    med = median(latencies)
    if med is not None:
        med = round(med, 2)

    return {'total_entries': total_entries, 'filtered_entries': len(filtered_logs), 'token_threshold': threshold,
            'total_tokens': total_tokens, 'avg_latency_ms': average, 'extra_latency_metric': {'name': 'median_latency_ms', 'value': med}, 'quantity_errors': quantity_errors}

def median(values):
    if not values:
        return None
    elif len(values) % 2 == 1:
        sorted_values = sorted(values)
        return sorted_values[len(sorted_values) // 2]
    else:
        sorted_values = sorted(values)
        medium_1 = sorted_values[len(sorted_values) // 2]
        medium_2 = sorted_values[len(sorted_values) // 2 - 1]
        return (medium_1 + medium_2) / 2

def is_number(value):
    if isinstance(value, bool):
        return False
    elif isinstance(value, (int, float)):
        return True
    else:
        return False

def main():
    try:
        logs = load_logs("data/logs.json")
        print("Всего логов:", len(logs))
        filtered_logs = filter_logs(logs, TOKEN_THRESHOLD)
        if len(filtered_logs) == 0:
            print("ни у одной записи нет tokens_used или они ниже порога:", TOKEN_THRESHOLD, file=sys.stderr)
        print("Прошло фильтр:", len(filtered_logs))
        os.makedirs("results", exist_ok=True)
        save_filtered(filtered_logs)
        print("Порог токенов:", TOKEN_THRESHOLD)
        report = calculate_metrics(filtered_logs, len(logs), TOKEN_THRESHOLD)
        print(report)
        save_report(report)

    except FileNotFoundError:
        print("Ошибка: путь или файл не найден", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("Ошибка: в строке невалидный JSON", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()