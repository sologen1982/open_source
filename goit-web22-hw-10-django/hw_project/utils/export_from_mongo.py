import pymongo
import json

# Підключення до MongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost")
mongo_db = mongo_client["hw"]

# Експорт даних з колекції "authors"
authors = list(mongo_db.authors.find())
with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(authors, f, default=str, ensure_ascii=False, indent=4)

# Експорт даних з колекції "quotes"
quotes = list(mongo_db.quotes.find())
with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes, f, default=str, ensure_ascii=False, indent=4)

print("Дані експортовано успішно.")
