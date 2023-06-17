from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
import sqlite3
app = Flask(__name__)
app.secret_key = 'many random bytes'
DATABASE = 'crud.db'
def create_table():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
create_table()
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/')
def Index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', students=data)
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO students (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('Index'))
@app.route('/delete/<int:id_data>', methods=['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (id_data,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('Index'))
@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        UPDATE students SET name=?, email=?, phone=?
        WHERE id=?
        """, (name, email, phone, id_data))
        conn.commit()
        cur.close()
        conn.close()
        flash("Data Updated Successfully")
        return redirect(url_for('Index'))
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)