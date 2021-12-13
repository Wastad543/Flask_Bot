from flask import Flask, render_template, request, redirect
import psycopg2
import requests

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="2003",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

#login
@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            
            username = request.form.get('username')
            password = request.form.get('password')

            #Исключение пустых полей
            if len(username)==0 or len(password)==0:
                return render_template('error.html')

            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = cursor.fetchall()

            #Исключение отсутсвия пользователя
            if len(records)==0:
                return render_template('error.html')

            return render_template('account.html', full_name=records[0][1], login='login: '+str(username), password='password: '+str(password))

        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

#Register
@app.route('/registration/', methods=['POST', 'GET'])
def registration():

    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        
        #Исключение на пустые поля
        cursor.execute("SELECT * FROM service.users WHERE login='"+str(login)+"';")

        if len(name)==0 or len(login)==0 or len(password)==0:
            return render_template('error.html')

        #Исключение на пользователя с таким же логином
        elif len(cursor.fetchall()):
            return render_template('error.html')
        else:
            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);', (str(name), str(login), str(password)))

            conn.commit()

            return redirect('/login/')

    return render_template('registration.html')
