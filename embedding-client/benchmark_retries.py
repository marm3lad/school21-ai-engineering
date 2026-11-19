import time
from embedding_client import get_embedding

N_REQUESTS = 100
CONFIGS = [
    {"name": "retries_0", "max_retries": 0, "delay": 0.1, "multiplier": 2},
    {"name": "retries_1", "max_retries": 1, "delay": 0.1, "multiplier": 2},
    {"name": "retries_2", "max_retries": 2, "delay": 0.2, "multiplier": 2},
]

def run_benchmark(config):
    start = time.perf_counter()
    successes = 0
    failures = 0
    for _ in range(N_REQUESTS):
        try:
            get_embedding("случайно", config)
            successes += 1
        except Exception:
            failures += 1

    elapsed = time.perf_counter() - start
    return {"name": config["name"], "elapsed": round(elapsed, 2), "average": round(elapsed / N_REQUESTS, 3), "successes": successes, "failures": failures}

if __name__ == "__main__":
    for config in CONFIGS:
        print(run_benchmark(config))

