from flask import jsonify


class Book:
    isbn = ""
    title = ""
    author = ""
    publisher = ""
    pub_date = ""
    information = ""
    img_url = ""

    def __init__(self, isbn, title, author, publisher, pub_date, information, img_url):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.pub_date = pub_date
        self.information = information
        self.img_url = img_url

    def read(self):
        return jsonify({
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "pubDate": self.pub_date,
            "information": self.information,
            "imgUrl": self.img_url
        })
