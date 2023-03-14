from elasticsearch import Elasticsearch, helpers
import pandas as pd
import json
#TODO: 개선 필요
document = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas":0,
        "analysis": {
            "tokenizer": {
                "nori_none": {
                    "type": "nori_tokenizer",
                    "decompound_mode": "none"
                },
                "nori_mixed": {
                    "type": "nori_tokenizer",
                    "decompound_mode": "mixed"
                },
                "nori_discard": {
                    "type": "nori_tokenizer",
                    "decompound_mode": "discard"
                },
            },
            "analyzer": {
                "nori_none": {
                    "type": "custom",
                    "tokenizer": "nori_none",
                    "filter": ["lowercase", "nori-readingform"]
                },
                "nori_mixed": {
                    "type": "custom",
                    "tokenizer": "nori_mixed",
                    "filter": ["lowercase", "nori-readingform"]
                },
                "nori_discard": {
                    "type": "custom",
                    "tokenizer": "nori_discard",
                    "filter": ["lowercase", "nori-readingform"]
                },
            }
        }
    },
    "mappings": {
        "properties": {
            "author": {
                "type": "text",
                "analyzer": "nori_mixed",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "img_url": {
                "type": "text",
                "analyzer": "nori_mixed",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "information": {
                "type": "text",
                "analyzer": "nori_mixed",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "isbn": {
                "type": "text",
                "analyzer": "nori_mixed",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "pub_date": {
                "type": "text",
                "analyzer": "nori_mixed",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "publisher": {
                "type": "text",
                "analyzer": "nori_mixed",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "title": {
                "type": "text",
                "analyzer": "nori_mixed",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            }
        }
    }
}

def index(es_cli=None, body=None):
    if not es_cli.indices.exists(index="books"):
        es_cli.indices.create(index="books", body=body)

if __name__ == '__main__':
    es = Elasticsearch("localhost:9200", timeout=30)
    index(es, json.dumps(document))

    for chunk in pd.read_csv('/Users/namjihyeon/bookclub/book_202112.csv', chunksize=1000):
        chunk.drop(columns=["SEQ_NO", "VLM_NM", "PBLICTE_DE", "ADTION_SMBL_NM", "PRC_VALUE", "KDC_NM",
                                    "TITLE_SBST_NM", "AUTHR_SBST_NM", "INTNT_BOOKST_BOOK_EXST_AT",
                                    "PORTAL_SITE_BOOK_EXST_AT", "ISBN_NO"], inplace=True)
        chunk.drop(chunk[chunk["BOOK_INTRCN_CN"].isna()].index, inplace=True)
        chunk.rename(columns={
                            "ISBN_THIRTEEN_NO": "isbn",
                            "TITLE_NM": "title",
                            "AUTHR_NM": "author",
                            "PUBLISHER_NM": "publisher",
                            "IMAGE_URL": "img_url",
                            "BOOK_INTRCN_CN": "information",
                            "TWO_PBLICTE_DE": "pub_date"
                    }, inplace=True
        )
#        print(json.loads(chunk.to_json(orient='records')))
#        es.index(index="books", doc_type="_doc", body=json.loads(chunk.to_json(orient='records')))
        helpers.bulk(es, chunk, index="books")
    print(chunk.head())
