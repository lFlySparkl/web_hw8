import json
import redis
from mongoengine import connect
from models import Author, Quote

# Підключення до Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def search_quotes(command, value):
    command = command.lower().strip()
    
    # Перевірка кешу Redis
    cache_key = f"{command}:{value}"
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return Quote.objects(id__in=json.loads(cached_result.decode('utf-8')))

    if command == 'name':
        # Пошук за ім'ям автора з можливістю скороченого запису
        regex_pattern = f'^{value}'  # Регулярний вираз для початку значення
        authors = Author.objects(fullname__iregex=regex_pattern)
        if authors:
            author_ids = [author.id for author in authors]
            quotes = Quote.objects(author__in=author_ids)
            # Збереження результатів у кеш Redis
            redis_client.set(cache_key, json.dumps([str(quote.id) for quote in quotes]))
            return quotes
        else:
            return None
    elif command == 'tag':
        # Пошук за тегом з можливістю скороченого запису
        regex_pattern = f'^{value}'  # Регулярний вираз для початку значення
        quotes = Quote.objects(tags__iregex=regex_pattern)
        # Збереження результатів у кеш Redis
        redis_client.set(cache_key, json.dumps([str(quote.id) for quote in quotes]))
        return quotes
    elif command == 'tags':
        # Пошук за набором тегів
        tags_list = value.split(',')
        quotes = Quote.objects(tags__iexact__in=tags_list)
        return quotes
    else:
        return None

def print_quotes(quotes):
    if quotes:
        for quote in quotes:
            print(f"Author: {quote.author.fullname}")
            print(f"Quote: {quote.quote}")
            print(f"Tags: {', '.join(quote.tags)}\n")
    else:
        print("No quotes found.")

def main():
    connect(
        db='my_mongodb',
        host='mongodb://localhost:27017',
    )

    while True:
        user_input = input("Enter command (type 'help' for instructions): ").strip().lower()
        if ':' in user_input:
            command, value = user_input.split(':')
            quotes = search_quotes(command.strip(), value.strip())
            print_quotes(quotes)
        elif user_input == "help":
            print("Commands:")
            print("name: <author_name> - Search for quotes by author name")
            print("tag: <tag> - Search for quotes by tag")
            print("tags: <tag1,tag2> - Search for quotes by a set of tags")
            print("exit - Exit the script")
        elif user_input == "exit":
            break
        else:
            print("Invalid command. Type 'help' for instructions.")

if __name__ == '__main__':
    main()
