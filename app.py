from flask import Flask
from book import Book
from search import search

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/book')
def read_book():
    new_book = Book("9791156759270",
                    "너에게 목소리를 보낼게 - <달빛천사> 성우 이용신의 첫 번째 에세이",
                    "이용신", "푸른숲", "2021-12-03",
                    "2004년 방영한 애니메이션 <달빛천사>에서 주인공 루나(풀문) 역을 맡으며 90년대생들에게 보석 같은 추억을 선물한 성우 이용신의 첫 번째 에세이. 수많은 작품의 주연을 맡으며 쉬지 않고 대중에게 행복을 전해온 성우 이용신의 발자취를 확인할 수 있다.",
                    "https://image.aladin.co.kr/product/28415/8/cover/k652835115_1.jpg")
    return new_book.read()

@app.route('/test')
def test():
    result = search('books')
    hits = result['hits']['hits']
    print(len(hits))

if __name__ == '__main__':
    app.run()
