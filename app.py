from flask import Flask, request, jsonify
from search import search_by_title

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/title', methods=['POST'])
def search():
    keyword = request.get_json()['keyword']
    num, result = search_by_title(keyword)
    return jsonify({
        "total": num,
        "result": result
    })

@app.route('/isbn', methods=['POST'])
def search_by_isbn():
    print()


if __name__ == '__main__':
    app.run()
