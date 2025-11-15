import time
import requests
import threading

URLS = [
    "https://www.example.com",
    "https://www.example.org",
    "https://www.example.net",
    "https://www.example.edu",
]


def fetch_url(url):
    response = requests.get(url)
    return len(response.content)  # Return content size

def fetch_url_thread(url, results, index):
    response = requests.get(url)
    results[index] = len(response.content)


def main():
    start_time = time.time()
    results = [fetch_url(url) for url in URLS]
    end_time = time.time()
    print("Sequential Execution Time:", end_time - start_time)

    start_time = time.time()
    threads = []
    results = [''] * len(URLS)
    for i, url in enumerate(URLS):
        t = threading.Thread(target=fetch_url_thread, args=(url, results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()
    print("Sequential Execution Time:", end_time - start_time)


if __name__ == "__main__":
    main()
