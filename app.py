from flask import Flask, render_template, request, redirect
import sqlite3
import os 

app = Flask(__name__)

def init_db():
    with sqlite3.connect('students.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students(
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
        conn.execute('INSERT INTO students (name, course) VALUES (?, ?)', (name, course))
    return redirect('/')

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    with sqlite3.connect('students.db') as conn:
        if request.method == 'POST':
            name = request.form['name']
            course = request.form['course']
            conn.execute('UPDATE students SET name=?, course=? WHERE id=?', (name, course, id))
            return redirect('/')
        student = conn.execute('SELECT * FROM students WHERE id=?', (id,)).fetchone()
        return render_template('edit.html', student=student)

@app.route('/delete/<int:id>')
def delete(id):
    with sqlite3.connect('students.db') as conn:
        conn.execute('DELETE FROM students WHERE id=?', (id,))
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


    <!DOCTYPE html>
<html>
<head><title>Student List</title></head>
<body>
  <h1>Student List</h1>
  
  <form method="POST" action="/add">
    <input name="name" placeholder="Name" required>
    <input name="course" placeholder="Course" required>
    <button type="submit">Add Student</button>
  </form>

  <ul>
    {% for s in students %}
      <li>{{ s[1] }} ({{ s[2] }})
        <a href="/edit/{{ s[0] }}">Edit</a>
        <a href="/delete/{{ s[0] }}">Delete</a>
      </li>
    {% endfor %}
  </ul>

  <br>
  
</body>
</html>


<!DOCTYPE html>
<html>
<head><title>Edit Student</title></head>
<body>
  <h1>Edit Student</h1>

  <form method="POST">
    <input name="name" value="{{ student[1] }}" required>
    <input name="course" value="{{ student[2] }}" required>
    <button type="submit">Save Changes</button>
  </form>

  <br>
  
</body>
</html>



