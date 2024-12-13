import sqlite3
from flask import Flask, flash, get_flashed_messages, redirect, render_template, request,session, url_for
app = Flask(__name__)
app.secret_key=('lilbillsgotohome')
from data import init_db

init_db()
@app.route('/')
def index():
    if 'user' in session:
        return render_template('main.html')
    else:
        return render_template('login.html')

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username =? AND password = ?", (username,password))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            session['user'] = username
            return redirect("/")
        else:
            flash("Неправильний логін або пароль",'error')
            return redirect('/login')
    else:
        return render_template('login.html')
            
        
    
@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
            conn.commit()
            flash("Реєстрація успішна",'info')
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash("Користувач з таким іменем вже існує",'error')
            return redirect('/register')
    else:
        return render_template('register.html')
@app.route('/logout')
def logout():
    session.pop('user',None)
    get_flashed_messages()
    return redirect('/login')
    
app.run()