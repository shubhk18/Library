from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize the SQLite database
DATABASE = 'app.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Create users table
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')
        # Create books table
        cursor.execute('''CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')
        # Add a default admin user
        cursor.execute('''INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)''', ('admin', 'password'))
        conn.commit()

init_db()

@app.route('/')
def home():
    if 'username' in session:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT books.title, books.author, users.username FROM books 
                              JOIN users ON books.user_id = users.id''')
            books = cursor.fetchall()
        return render_template('home.html', username=session['username'], books=books)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()
            if user:
                session['username'] = username
                session['user_id'] = user[0]
                return redirect(url_for('home'))
        return 'Invalid credentials!'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                return 'Username already exists!'
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login', message='You have been logged out.'))

@app.route('/add_book', methods=['POST'])
def add_book():
    if 'username' in session:
        title = request.form['title']
        author = request.form['author']
        user_id = session['user_id']
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO books (title, author, user_id) VALUES (?, ?, ?)', (title, author, user_id))
            conn.commit()
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/books')
def books():
    if 'username' in session:
        user_id = session['user_id']
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT title, author, id FROM books WHERE user_id = ?''', (user_id,))
            books = cursor.fetchall()
        return render_template('books.html', books=books)
    return redirect(url_for('login'))

@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    if 'username' in session:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM books WHERE id = ? AND user_id = ?', (book_id, session['user_id']))
            conn.commit()
        return redirect(url_for('home'))
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)