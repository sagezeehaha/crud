from flask import Flask, render_template, redirect, request
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('students.db') as conn:
        conn.execute ('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                course TEXT
            )
        ''')

@app.route('/')
def index():
    with sqlite3.connect('students.db') as conn:
        students = conn.execute('SELECT * FROM students').fetchall()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    course = request.form['course']
    with sqlite3.connect('students.db') as conn:
        conn.execute ('INSERT INTO students (name, course) VALUES (?, ?)', (name, course))
    return redirect ('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    with sqlite3.connect('students.db') as conn:
        if request.method == 'POST':
            name = request.form['name']
            course = request.form['course']
            conn.execute('UPDATE students SET name=?, course=? WHERE id=?', (name, course, id))
            return redirect('/')
        student = conn.execute('SELECT * FROM students WHERE id=?', (id,)).fetchone()
    return render_template('edit.html', students=students)

@app.route('/delete/<int:id>')
def delete(id):
    with sqlite3.connect('students.db') as conn:
        conn.execute('DELETE FROM students WHERE id=?', (id,))
    return redirect('/')

if __name__ =='__main__':
    init_db()
    app.run(debug=True)