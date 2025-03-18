from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

from config import MYSQL_CONFIG

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Verificar en la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return "Bienvenido"
    return "Credenciales incorrectas"
