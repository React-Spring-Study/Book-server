from elasticsearch import Elasticsearch
from book import Book

index = "books"

def search_by_title(title):
    es = Elasticsearch("localhost:9200", timeout=30)
    body = {
        'size': 20,
        'query': {
            'match': {
                'title': title
            }
        }
    }
    result = es.search(index=index, body=body)['hits']
    total = result['total']['value']
    return total, to_book(result)


def search_by_isbn(isbn):
    es = Elasticsearch("localhost:9200", timeout=30)
    body = {
        "query": {
            "bool": {
                "filter": [
                    {
                        "match": {
                            "isbn.keyword": isbn
                        }
                    }
                ]
            }
        }
    }
    result = es.search(index=index, body=body)['hits']
    return to_book(result)

def to_book(result):
    response = []
    for book in result['hits']:
        response.append(
            Book(book['_source']['isbn'],
                 book['_source']['title'],
                 book['_source']['author'],
                 book['_source']['publisher'],
                 book['_source']['pub_date'],
                 book['_source']['information'],
                 book['_source']['img_url']).serialize()
        )
    return response


