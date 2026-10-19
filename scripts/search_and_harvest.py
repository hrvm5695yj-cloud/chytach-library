import os
import json
import requests

# Список ключових тем для пошуку навчальних матеріалів, НМТ, Біблії та казок
SEARCH_QUERIES = [
    "НМТ українська мова література",
    "Шкільна програма хрестоматія",
    "Українські народні казки",
    "Буквар українська мова",
    "Біблія"
]

def search_and_harvest():
    catalog = []
    seen_urls = set()
    
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
                    
                    # Пріоритет форматыв: EPUB -> PDF -> TXT
                    download_url = (
                        formats.get('application/epub+zip') or 
                        formats.get('application/pdf') or 
                        formats.get('text/plain; charset=utf-8') or
                        formats.get('text/plain')
                    )
                    
                    if download_url and download_url not in seen_urls:
                        seen_urls.add(download_url)
                        catalog.append({
                            "id": str(book.get('id')),
                            "title": title,
                            "author": authors,
                            "url": download_url,
                            "category": "Навчання / Книги / Біблія"
                        })
        except Exception as e:
            print(f"Помилка при запиті {query}: {e}")

    # Зберігаємо результат у catalog.json для автоматичного оновлення
    with open("catalog.json", "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    
    print(f"Категоризовано та збережено книг: {len(catalog)}")

if __name__ == "__main__":
    search_and_harvest()
