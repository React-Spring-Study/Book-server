from elasticsearch import Elasticsearch
from book import Book

index = "books"
es = Elasticsearch("localhost:9200", timeout=30)


# 책 제목 검색
def search_by_title(title):
    body = {
        'size': 10,
        'query': {
            'match': {
                'title': title
            }
        }
    }
    result = es.search(index=index, body=body)['hits']
    total = result['total']['value']
    return total, to_book(result)

# 책 추천
def recommend(isbn):
    book = search_by_isbn(isbn)
    if book is not None:
        return recommend_by_information(book[0]['_source']['information'])

# - isbn 으로 검색
def search_by_isbn(isbn):
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
    result = es.search(index=index, body=body)['hits']['hits']
    if len(result) == 0:
        return
    return result
    # 리스트

# - 실질적 추천 로직
def recommend_by_information(text):
    body = {
        'size': 4,
        'query': {
            'match': {
                'information': text
            }
        }
    }
    result = es.search(index=index, body=body)['hits']
    return to_book_without_me(result)

# 테스트용: 책 소개로 검색
def search_by_information(text):
    body = {
        'size': 10,
        'query': {
            'match': {
                'information': text
            }
        }
    }
    result = es.search(index=index, body=body)['hits']
    response = []
    for book in result['hits']:
        response.append(
            {
                "book": Book(book['_source']['isbn'],
                             book['_source']['title'],
                             book['_source']['author'],
                             book['_source']['publisher'],
                             book['_source']['pub_date'],
                             book['_source']['information'],
                             book['_source']['img_url']).serialize_info(),
                "score": book['_score']
            }
        )
    return response

# 응답용 객체 생성
def to_book(result):
    response = []
    for book in result['hits']:
        response.append(
            {
                "book": Book(book['_source']['isbn'],
                             book['_source']['title'],
                             book['_source']['author'],
                             book['_source']['publisher'],
                             book['_source']['pub_date'],
                             book['_source']['information'],
                             book['_source']['img_url']).serialize(),
                "score": book['_score']
            }
        )
    return response

def to_book_without_me(result):
    response = []
    for book in result['hits']:
        response.append(
            {
                "book": Book(book['_source']['isbn'],
                             book['_source']['title'],
                             book['_source']['author'],
                             book['_source']['publisher'],
                             book['_source']['pub_date'],
                             book['_source']['information'],
                             book['_source']['img_url']).serialize(),
                "score": book['_score']
            }
        )
    response.pop(0)
    return response


