import json
import os
from mongoengine import connect
from models import Author, Quote

def load_data():
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # Завантаження авторів
    authors_path = os.path.join(current_directory, 'json', 'authors.json')
    with open(authors_path, 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        Author.objects.insert([Author(**author_data) for author_data in authors_data])

    # Завантаження цитат
    quotes_path = os.path.join(current_directory, 'json', 'quotes.json')
    with open(quotes_path, 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author_name = quote_data.pop('author')
            author = Author.objects(fullname=author_name).first()
            if author:
                # Якщо автор існує, створіть ReferenceField для автора у моделі Quote
                quote_data['author'] = author
                Quote(**quote_data).save()

def main():
    connect(
        db='my_mongodb',
        host='mongodb://localhost:27017',
    )
    load_data()

if __name__ == '__main__':
    main()
