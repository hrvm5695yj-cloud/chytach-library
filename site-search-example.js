// Додай цей код у фронтенд Netlify або адаптуй до наявного index.html.
// Замінити YOUR-GITHUB-USERNAME на свій логін GitHub.
const CATALOG_URL = "https://raw.githubusercontent.com/YOUR-GITHUB-USERNAME/chytach-library/main/catalog.json";
const BOOKS_BASE_URL = "https://raw.githubusercontent.com/YOUR-GITHUB-USERNAME/chytach-library/main/";

function normalizeUa(value = "") {
  return value.toLocaleLowerCase("uk-UA")
    .normalize("NFD").replace(/[\u0300-\\u036f]/g, "")
    .replace(/[’ʼ`]/g, "'").replace(/[^a-zа-яіїєґ0-9\s'-]/gi, " ")
    .replace(/\s+/g, " ").trim();
}

async function loadCatalog() {
  const res = await fetch(CATALOG_URL, { cache: "no-store" });
  if (!res.ok) throw new Error("Не вдалося завантажити каталог");
  return (await res.json()).books || [];
}

function searchBooks(books, query = "", category = "") {
  const q = normalizeUa(query);
  return books.filter(book => {
    const all = normalizeUa([book.title, book.author, ...(book.categories || []), ...(book.sourceCategories || [])].join(" "));
    const wordsMatch = !q || q.split(" ").filter(Boolean).every(word => all.includes(word));
    return wordsMatch && (!category || (book.categories || []).includes(category));
  });
}

function bookUrl(book) {
  return BOOKS_BASE_URL + book.file;
}

async function previewBook(book) {
  const res = await fetch(bookUrl(book));
  if (!res.ok) throw new Error("Файл книжки поки недоступний");
  return await res.text();
}

function downloadBook(book) {
  const a = document.createElement("a");
  a.href = bookUrl(book);
  a.download = `${book.title}.txt`;
  a.rel = "noopener";
  document.body.appendChild(a);
  a.click();
  a.remove();
}

// Використання:
// const books = await loadCatalog();
// const results = searchBooks(books, "ліс", "Романи");
// const text = await previewBook(results[0]);
// downloadBook(results[0]);
