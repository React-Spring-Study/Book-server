from flask import Flask, request, jsonify
from search import search_by_title, recommend, search_by_isbn, search_by_information
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

CORS(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/title', methods=['POST'])
def search_title():
    keyword = request.get_json()['keyword']
    num, result = search_by_title(keyword)
    return jsonify({
        "total": num,
        "result": result
    })

@app.route('/test', methods=['POST'])
def search_recommend():
    isbn = request.get_json()['isbn']
    result = recommend(isbn)
    return jsonify({"result": result})

@app.route('/isbn', methods=['POST'])
def search_isbn():
    isbn = request.get_json()['isbn']
    result = search_by_isbn(isbn)
    return jsonify({"result": result})

@app.route('/info', methods=['POST'])
def search_info():
    info = request.get_json()['information']
    result = search_by_information(info)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
