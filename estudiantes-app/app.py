import os
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = 'database.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER,
            carrera TEXT,
            correo TEXT
        )
        """)

@app.route('/')
def index():
    with sqlite3.connect(DB) as conn:
        estudiantes = conn.execute("SELECT * FROM estudiantes").fetchall()
    return render_template('index.html', estudiantes=estudiantes)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        carrera = request.form['carrera']
        correo = request.form['correo']
        with sqlite3.connect(DB) as conn:
            conn.execute("INSERT INTO estudiantes (nombre, edad, carrera, correo) VALUES (?, ?, ?, ?)",
                         (nombre, edad, carrera, correo))
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    with sqlite3.connect(DB) as conn:
        estudiante = conn.execute("SELECT * FROM estudiantes WHERE id = ?", (id,)).fetchone()
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        carrera = request.form['carrera']
        correo = request.form['correo']
        with sqlite3.connect(DB) as conn:
            conn.execute("UPDATE estudiantes SET nombre=?, edad=?, carrera=?, correo=? WHERE id=?",
                         (nombre, edad, carrera, correo, id))
        return redirect(url_for('index'))
    return render_template('edit.html', estudiante=estudiante)

@app.route('/delete/<int:id>')
def delete(id):
    with sqlite3.connect(DB) as conn:
        conn.execute("DELETE FROM estudiantes WHERE id = ?", (id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
