import requests
import time
import sys

URL = "http://127.0.0.1:5000/embed"
DEFAULT_RETRY_CONFIG = {"max_retries": 2, "delay": 1, "multiplier": 2}

def get_embedding(text, retry_config=None):
    if retry_config is None:
        retry_config = DEFAULT_RETRY_CONFIG
    max_retries = retry_config["max_retries"]
    delay = retry_config["delay"]
    multiplier = retry_config["multiplier"]
    rest = delay
    for attempt in range(max_retries + 1):
        try:
            response = requests.post(URL, json={"text": text}, timeout=2)
            if response.status_code == 200:
                return response.json()["embedding"]
            elif response.status_code in (429, 500, 503):
                if attempt < max_retries:
                    print(f"попытка {attempt + 1}: ошибка {response.status_code}, ожидание: {rest} сек", file=sys.stderr)
                    time.sleep(rest)
                    rest *= multiplier
                continue
            else:
                raise Exception("ошибка сервера: " + str(response.status_code))
        except requests.exceptions.Timeout:
            if attempt < max_retries:
                print(f"попытка {attempt + 1}: временный таймаут, ожидание: {rest} сек",
                      file=sys.stderr, sep="")
                time.sleep(rest)
                rest *= multiplier
            continue
    raise Exception("все попытки исчерпаны")

if __name__ == "__main__":
    texts = ["привет", "сбой500", "сбой429", "сбой503", "медленно", "", "как дела"]
    for text in texts:
        try:
            embedding = get_embedding(text)
            print(f"'{text}': успех, первые числа: {embedding[:3]}")
        except Exception as e:
            print(f"'{text}': не получилось, {e}")