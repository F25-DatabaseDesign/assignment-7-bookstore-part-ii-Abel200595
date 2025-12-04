from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)
def get_db_connection():
    conn = sqlite3.connect('bookstore.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_categories():
    conn=get_db_connection()
    categories=conn.execute("""select * from categories""").fetchall()
    conn.close()
    return categories

@app.route('/')
def home():
    return render_template("index.html", categories=get_categories())

@app.route('/category/<int:category_id>')
def category(category_id):
    conn=get_db_connection()
    books=conn.execute("""select * from books where categoryId=?""",(category_id,)).fetchall()
    conn.close()
    return render_template("category.html",books=books,categories=get_categories(),selectedCategory=category_id)

@app.errorhandler(Exception)
def handle_error(e):
    return render_template("error.html", error=e)

@app.route("/search",methods=["post"])
def search():
    term=request.form.get("search","").strip()
    query=f"%{term.lower()}%"
    conn=get_db_connection()
    books=conn.execute("""
                        select 
                            books.*,
                            categories.name as categoryName
                        from books
                        join categories on categories.id=books.categoryId
                        where 
                             lower(books.title) like ?
                             or lower(books.isbn) like ?
                             or lower(books.author) like ?
                             or lower(categories.name) like ?
                        """, (query,query,query,query)).fetchall()
    conn.close()
    return render_template("search.html",books=books,categories=get_categories(),term=term)
                             
@app.route("/book/<int:book_id>")
def book_detail(book_id):
    conn=get_db_connection()
    book=conn.execute("""select books.*,categories.name as categoryName
                       from books
                       join categories on categories.id=books.categoryId
                       where books.id=?""",(book_id,)).fetchone()
    conn.close()
    return render_template("book_detail.html",book=book,categories=get_categories())
    
                       


if __name__ == "__main__":
    app.run(debug=True)
    

