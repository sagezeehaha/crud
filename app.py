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

<!DOCTYPE html>
<html>
<head>
  <title>Students</title>
  <style>
  body {
    font-family: Arial, sans-serif;
    padding: 30px;
    background-color: #f5f5f5;
  }

  h1 {
    color: #333;
  }

  form {
    margin-bottom: 20px;
  }

  input {
    padding: 8px;
    margin-right: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  button {
    padding: 8px 12px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  button:hover {
    background-color: #45a049;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    margin-bottom: 10px;
    background: white;
    padding: 10px;
    border-radius: 5px;
    box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.1);
  }

  a {
    margin-left: 10px;
    text-decoration: none;
    color: #007BFF;
  }

  a:hover {
    text-decoration: underline;
  }
</style>

</head>
<body>
  <h1>Student List</h1>

  <form action="/add" method="POST">
    <input name="name" placeholder="Name" required>
    <input name="course" placeholder="Course" required>
    <button type="submit">Add Student</button>
  </form>

  <ul>
    {% for s in students %}
      <li>
        {{ s[1] }} - {{ s[2] }}
        <a href="/edit/{{ s[0] }}">Edit</a>
        <a href="/delete/{{ s[0] }}">Delete</a>
      </li>
    {% endfor %}
  </ul>
</body>
</html>

<!DOCTYPE html>
<html>
<head>
    <title>Students</title>
    <style>
  body {
    font-family: Arial, sans-serif;
    padding: 30px;
    background-color: #f5f5f5;
  }

  h1 {
    color: #333;
  }

  form {
    margin-bottom: 20px;
  }

  input {
    padding: 8px;
    margin-right: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  button {
    padding: 8px 12px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  button:hover {
    background-color: #45a049;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    margin-bottom: 10px;
    background: white;
    padding: 10px;
    border-radius: 5px;
    box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.1);
  }

  a {
    margin-left: 10px;
    text-decoration: none;
    color: #007BFF;
  }

  a:hover {
    text-decoration: underline;
  }
</style>

</head>
<body>
  <h1>Student List</h1>

  <form action="/add" method="POST">
    <input name="name" placeholder="Name" required>
    <input name="course" placeholder="Course" required>
    <button type="submit">Add Student</button>
  </form>

  <ul>
    {% for s in students %}
      <li>
        {{ s[1] }} - {{ s[2] }}
        <a href="/edit/{{ s[0] }}">Edit</a>
        <a href="/delete/{{ s[0] }}">Delete</a>
      </li>
    {% endfor %}
  </ul>
</body>
</html>		
