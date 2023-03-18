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

    def serialize(self):
        return {
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "pubDate": self.pub_date,
            "imgUrl": self.img_url
        }

    def serialize_info(self):
        return {
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "information": self.information,
            "pubDate": self.pub_date,
            "imgUrl": self.img_url
        }
