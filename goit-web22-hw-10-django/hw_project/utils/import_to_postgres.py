import json
import psycopg2

# Підключення до Postgres
pg_conn = psycopg2.connect(
    dbname="hw_10",
    user="postgres",
    password="0082",
    host="localhost"
)
pg_cursor = pg_conn.cursor()

# Імпорт даних авторів
with open('authors.json', 'r', encoding='utf-8') as f:
    authors = json.load(f)

for author in authors:
    pg_cursor.execute("""
        INSERT INTO authors (fullname, born_date, born_location, description)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (author['fullname'], author.get('born_date'), author.get('born_location'), author.get('description')))
    author_id = pg_cursor.fetchone()[0]
    author['_id'] = author_id

pg_conn.commit()

# Імпорт даних цитат
with open('quotes.json', 'r', encoding='utf-8') as f:
    quotes = json.load(f)

for quote in quotes:
    author_id = next((author['_id'] for author in authors if author['fullname'] == quote['author']), None)
    if author_id is not None:
        pg_cursor.execute("""
            INSERT INTO quotes (quote, author_id, tags)
            VALUES (%s, %s, %s)
        """, (quote['quote'], author_id, quote['tags']))

pg_conn.commit()

print("Дані імпортовано успішно.")
pg_cursor.close()
pg_conn.close()
