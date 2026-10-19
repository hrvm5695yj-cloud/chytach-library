import os
import json
import requests

# Список ключових тем для пошуку навчальних матеріалів, НМТ та казок
SEARCH_QUERIES = [
    "НМТ українська мова література",
    "Шкільна програма хрестоматія",
    "Українські народні казки",
    "Буквар українська мова"
]

def search_and_harvest():
    catalog = []
    
    for query in SEARCH_QUERIES:
        print(f"Шукаю матеріали за запитом: {query}")
        url = f"https://gutendex.com/books/?search={requests.utils.quote(query)}"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for book in data.get('results', []):
                    title = book.get('title')
                    authors = ", ".join([a.get('name', '') for a in book.get('authors', [])])
                    formats = book.get('formats', {})
                    download_url = formats.get('application/epub+zip') or formats.get('text/plain; charset=utf-8')
                    
                    if download_url:
                        catalog.append({
                            "title": title,
                            "author": authors,
                            "url": download_url,
                            "category": "Навчання / НМТ / Казки"
                        })
        except Exception as e:
            print(f"Помилка при запиті {query}: {e}")

    # Зберігаємо результат у catalog.json, який автоматично підтягується в репозиторій
    with open("catalog.json", "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    
    print(f"Категоризовано та збережено книг: {len(catalog)}")

if __name__ == "__main__":
    search_and_harvest()
