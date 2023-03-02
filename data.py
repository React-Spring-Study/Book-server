from elasticsearch import Elasticsearch, helpers
import pandas as pd

document = {
    "settings": {
        "analysis": {
            "analyzer": {
                "content": {
                    "type": "custom",
                    "tokenizer": "nori_tokenizer",
                    "decompound_mode": "mixed"
                }
            }
        }
    },
    "mappings": {
        "book": {
            "properties": {
                "@timestamp": {
                    "type": "date"
                },
                "@version": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "author": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "host": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "id": {
                    "type": "long"
                },
                "img_url": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "information": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "isbn": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "message": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "path": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "pub_date": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "publisher": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "tags": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "title": {
                    "type": "text",
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
}

def index(es_cli=None, body=None):
    if not es_cli.indices.exists(index="books"):
        es_cli.indices.create(index="books", body=body)

if __name__ == '__main__':
    es = Elasticsearch("localhost:9200", timeout=30)
    index(es, document)
    """with open('/Users/namjihyeon/bookclub/book_202112.csv', mode='rt', encoding='UTF8') as f:
        reader = csv.DictReader(f)
        helpers.bulk(es, reader, index="books", raise_on_error=False)
        f.close()"""

    for chunk in pd.read_csv('/Users/namjihyeon/bookclub/book_202112.csv', chunksize=1000):
        chunk = chunk.drop(columns=["SEQ_NO", "VLM_NM", "PBLICTE_DE", "ADTION_SMBL_NM", "PRC_VALUE", "KDC_NM", "TITLE_SBST_NM",
                          "AUTHR_SBST_NM", "INTNT_BOOKST_BOOK_EXST_AT", "PORTAL_SITE_BOOK_EXST_AT", "ISBN_NO"])
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
    print(chunk.head())
