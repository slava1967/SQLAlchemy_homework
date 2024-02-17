from flask import Flask, render_template, request
from sqlalchemy import desc

from database import Book, Genre, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


@app.route("/", methods=["GET", "POST"])
def all_books():
    books = db.paginate(db.select(Book).order_by(desc(Book.added)), per_page=15, count=True)
    return render_template("all_books.html", books=books)


@app.route("/<int:book_id>", methods=["GET", "POST"])
def change_status(book_id):
    book = db.get_or_404(Book, book_id)
    if request.method == "POST":
        book.is_read = int(request.form['my_checkbox'])
        db.session.commit()
    return render_template("book.html", book=book)


@app.route("/genre/<int:genre_id>")
def books_by_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    return render_template(
        "books_by_genre.html",
        genre_name=genre.name,
        books=genre.books,
    )


if __name__ == "__main__":
    app.run()
