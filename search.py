from elasticsearch import Elasticsearch
import json

def issue(s, page=1, product=None, op=None, sort=None, ctgr=None):
    if product == 'All':
        product = None
    if page == None or "":
        doc_from, doc_to = 0, 10
    else:
        doc_from, doc_to = (int(page) - 1) * 10, (int(page)) * 10

    es_client = Elasticsearch("localhost:9200", timeout=30)

    with open('./body.json', mode='rt') as f:
        body = json.load(f)
        f.close()

    body['query']['bool']['must'][0]['bool']['should'][0]['multi_match'].update({"query": s})
    body['query']['bool']['must'][0]['bool']['should'][1]['match_phrase']['Issue Details'].update({"query": s})
    body['query']['bool']['must'][0]['bool']['should'][2]['match_phrase']['Action Log'].update({"query": s})
    body['query']['bool']['must'][0]['bool']['should'][3]['match_phrase']['Subject'].update({"query": s})
    body.update({"from": doc_from})

    if op == 'or':
        body['query']['bool']['must'][0]['bool']['should'][0]['multi_match'].update({"operator": op})

    if sort == 'latest':
        body.update({"sort": [{"Registered date": {"order": "desc"}}]})

    body['query']['bool']['filter'][0]['match'].update({"Product": product})
    body['query']['bool']['filter'][1]['terms'].update({"Category": ctgr})

    if product == None:
        body['query']['bool']['filter'].pop(0)

    response = es_client.search(index="issue-v0.1.4", body=body)
    hits = response['hits']['hits']
    total = response['hits']['total']['value']

    return hits, total

def search(index_name):
    es = Elasticsearch("localhost:9200", timeout=30)
    index=index_name
    body = {
        'query': {
            'match': {
                'title': '단어'
            }
        }
    }
    result = es.search(index=index, body=body)
    return result
