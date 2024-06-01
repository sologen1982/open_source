from typing import List, Any

import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_tags(tags: str) -> list[str | None]:
    print(f"Find by {tags}")
    tags_list = tags.split(',')
    quotes = Quote.objects(tags__in=tags_list)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author: str) -> list[list[Any]]:
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


def main():
    while True:
        command = input("Enter command (name: author | tag: tag | tags: tag1,tag2 | exit): ").strip()
        if command.startswith('name:'):
            name = command[len('name:'):].strip()
            quotes = find_by_author(name)
            for quote in quotes:
                print(quote)
        elif command.startswith('tag:'):
            tag = command[len('tag:'):].strip()
            quotes = find_by_tag(tag)
            for quote in quotes:
                print(quote)
        elif command.startswith('tags:'):
            tags = command[len('tags:'):].strip()
            quotes = find_by_tags(tags)
            for quote in quotes:
                print(quote)
        elif command == 'exit':
            break
        else:
            print("Unknown command")


if __name__ == '__main__':
    main()

    # print(find_by_tag('mi'))
    # print(find_by_tags('life,live'))

    # print(find_by_author('in'))
    # print(find_by_author('in'))
    # quotes = Quote.objects().all()
    # print([e.to_json() for e in quotes])
    # unique_tags = Quote.objects.distinct('tags')
    # print(unique_tags)
