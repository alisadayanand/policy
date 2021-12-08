from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('page1.html',title='Home Page')

@app.route('/base')
def base():
    return render_template('base1.html',title='Base Page')

@app.route('/viewbooks')
def View_Books():
    return render_template('viewbooks.html',title='View Books')

@app.route('/viewbooksbyisbn')
def View_Books_By_ISBN():
    return render_template('viewbooksbyisbn.html',title='View Books by ISBN')

@app.route('/updatebooks')
def Update_books():
    return render_template('updatebooks.html',title='Update Books')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        con = sqlite3.connect('user.db')
        cur = con.cursor()
        cur.execute('create table if not exists USER(name TEXT, password TEXT)')
        cur.execute('insert into USER values(?,?)', (name,password))
        con.commit()
        con.close()
        return redirect(url_for("showRegisterData"))

    return render_template('register.html',title='Register')

@app.route('/login', methods=['POST','GET'] )
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        con = sqlite3.connect('user.db')
        cur = con.cursor()
        listof_data = cur.execute('select * from USER')
        data = listof_data.fetchall()
        
        for i in range(len(data)):
            if name==data[i][0] and password==data[i][1]:
                print('welcome')
            else:
                print('incorrect')



    return render_template('login.html',title='Login')


@app.route('/registerdata')
def showRegisterData():
    #retrieve all data from database

    try:
        con = sqlite3.connect('user.db')
        cur = con.cursor() 
        listof_data = cur.execute('select * from USER')
        data = listof_data.fetchall()

        # for name,age in data:
        #     return name, str(age)
        # #return '{}'.format(data[0][0])
        return str(data)  
 
    except Exception as e:
        return "error in showing data"



app.run(port='8080',debug=True)