'''
Create a website where someone can apply for various policies.
The person should be able to
 - Login (Profile maintenance (CRUD)
 - Select policy (Policy maintenance (CRUD)
 - Complete the "purchase" of a policy 
 - View all the policies that the individual has taken out 
     - i.e all policies linked to a profile
	 - view details per policy	 
 
You will need to come up with the Front-end designs, APIs and database.
 
Use Flask, use grids, use flexbox, etc 
Use your process knowledge.

'''

from flask import Flask,render_template, redirect, url_for, request, json
import sqlite3

app = Flask(__name__)

# Every time a user reruns this code, make a connection to the database and drop the tables, 
# and recreate them with the same items every time

# connect to a database
con = sqlite3.connect('insurance.db')
cur = con.cursor()
# Drop tables at the start to ensure no repetition during testing --- This will change when deployed 

cur.execute('drop table if exists tbl_users')
cur.execute('drop table if exists tbl_policies')
cur.execute('drop table if exists tbl_usersPolicies')

# Create the tables again

cur.execute('create table if not exists tbl_users (userID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT , username TEXT UNIQUE, password TEXT, userType TEXT)')
                                                                                        # users name, unique username, password (meet criteria), customer or staff
cur.execute('create table if not exists tbl_policies (policyID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, category TEXT, premium NUMERIC)')
                                                                                                # Policy name, what it covers, its premium
cur.execute('create table if not exists tbl_usersPolicies (userPolicyID INTEGER PRIMARY KEY AUTOINCREMENT, userID INTEGER, policyName TEXT, dateTaken DATE)')
                                                        # like a transaction ID, what user it is, what policy it is, the date taken out on

# Staff members can only be added manually
users = [
    (1, 'Daniel Charters', 'dan', 'Password1', 'S'),
    (2, 'Mxolisi Ndlovu', 'Mx', 'Soccer10', 'C')
]

try:
    cur.executemany('insert into tbl_users values(?,?,?,?,?)', users)
except Exception as a:
    print(' error {}'.format(a))

policies = [
    (1, 'Sanlam life', 'Life', 450),
    (2, 'Sanlam home', 'Househod', 600),
    (3, 'Sanlam car', 'Car', 250)
]
try:
    cur.executemany('insert into tbl_policies values(?,?,?,?)', policies)
except Exception as a:
    print(' error {}'.format(a))

userPolicies = [
    (1, 2, 'Sanlam life', '2021-01-06'),
    (2, 2, 'Sanlam home', '2021-03-24')
]
try:
    cur.executemany('insert into tbl_usersPolicies values(?,?,?,?)', userPolicies)
except Exception as a:
    print(' error {}'.format(a))
    
con.commit()
con.close()


@app.route('/', methods =["POST","GET"])
@app.route('/home', methods =["POST","GET"])
def home():
    if request.method == "POST":
        pwd = request.form['Password']
        username = request.form['username']
        con = sqlite3.connect('insurance.db')
        cur = con.cursor()
        allUsers = cur.execute('select * from tbl_users where username = ?', (username,))
        users = allUsers.fetchone()
        con.close()
        if users is not None:
            if users[3] == pwd:
                if users[4] == 'S':
                    return redirect(url_for("afterLoginStaff", usersID = users[0]))
                else:
                    return redirect(url_for("afterLoginCustomer", usersID = users[0]))
            else:
                return render_template('home.html', LoginMessage = "INVALID CREDENTIALS.")
        else:
            return render_template('home.html', LoginMessage = "USERNAME NOT RECOGNISED.")
    else:
        return render_template('home.html', LoginMessage = "Welcome, please login below:")

@app.route('/afterLoginStaff/<usersID>', methods =["POST","GET"])
def afterLoginStaff(usersID):
    con = sqlite3.connect('insurance.db')
    cur = con.cursor()
    allUsers = cur.execute('select * from tbl_users where userID = ?', (usersID,))
    users = allUsers.fetchone()
    con.close()
    usersName = users[1]
    if request.method == "POST":
        choice = request.form['choice']
        if choice == "editPolicy":
            return redirect(url_for("editPolicy", usersID = users[0]))
        elif choice == "addPolicy":
            return redirect(url_for("addPolicy", usersID = users[0]))
        elif choice == "deletePolicy":
            return redirect(url_for("deletePolicy", usersID = users[0]))
        elif choice == "editUser":
            return redirect(url_for("editUser", usersID = users[0]))
        elif choice == "addUser":
            return redirect(url_for("addUser", usersID = users[0]))
        else:
            return redirect(url_for("deleteUser", usersID = users[0]))
            
    else:
        return render_template('staffAfterLogin.html', name= usersName )

@app.route('/editPolicies/<usersID>', methods =["POST","GET"])
def editPolicy(usersID):
    con = sqlite3.connect('insurance.db')
    cur = con.cursor()
    allUsers = cur.execute('select * from tbl_users where userID = ?', (usersID,))
    users = allUsers.fetchone()
    policyData = cur.execute('select * from tbl_policies')
    policiesData = policyData.fetchall()
    if request.method == "POST":
        chosenPolicy = request.form['policyToEdit']
        policyToEditData = cur.execute('select * from tbl_policies where name = ?', (chosenPolicy,))
        policyToEdit = policyToEditData.fetchone()
        name = policyToEdit[1]
        category = policyToEdit[2]
        premium = policyToEdit[3]
        F_name = request.form['policyName']
        F_category = request.form['policyCategory']
        F_premium = request.form['policyPremium']
        if F_name != '':
            name = F_name
        if F_category != '':
            category = F_category
        if F_premium != '':
            premium = F_premium
        cur.execute('update tbl_policies set name = ?, category = ?, premium = ? where name = ?',(name,category,premium,chosenPolicy))
        con.commit()
        policyData = cur.execute('select * from tbl_policies')
        policiesData = policyData.fetchall()
        con.close()
        return redirect(url_for("policies"))
    else:
        return render_template('staffEditPolicy.html', policies = policiesData)

@app.route('/addPolicies/<usersID>', methods =["POST","GET"])
def addPolicy(usersID):
    if request.method == "POST":
        F_name = request.form['policyName']
        F_category = request.form['policyCategory']
        F_premium = request.form['policyPremium']
        con = sqlite3.connect('insurance.db')
        cur = con.cursor()
        cur.execute('insert into tbl_policies values(null,?,?,?)', (F_name, F_category, F_premium))
        con.commit()
        policyData = cur.execute('select * from tbl_policies')
        policiesData = policyData.fetchall()
        con.close()
        return redirect(url_for("policies"))
    else:
        return render_template('staffAddPolicy.html')

@app.route('/deletePolicies/<usersID>', methods =["POST","GET"])
def deletePolicy(usersID):
    con = sqlite3.connect('insurance.db')
    cur = con.cursor()
    policyData = cur.execute('select * from tbl_policies')
    policiesData = policyData.fetchall()
    if request.method == "POST":
        F_name = request.form['policyToDelete']
        cur.execute('delete from tbl_policies where name = ?', (F_name, ))
        con.commit()
        policyData = cur.execute('select * from tbl_policies')
        policiesData = policyData.fetchall()
        con.close()
        return redirect(url_for("policies"))
    else:
        return render_template('staffDeletePolicy.html', policies = policiesData)
    
@app.route('/addUser/<usersID>', methods =["POST","GET"])
def addUser(usersID):
    if request.method == "POST":
        con = sqlite3.connect('insurance.db')
        cur = con.cursor()
        usersData = cur.execute('select * from tbl_users')
        userData = usersData.fetchall()
        F_name = request.form['name']
        F_username = request.form['username']
        F_password = request.form['password']
        F_staffType = request.form['staffType']
        cur.execute('insert into tbl_users values(null,?,?,?,?)', (F_name, F_username, F_password, F_staffType))
        con.commit()
        usersData = cur.execute('select * from tbl_users')
        userData = usersData.fetchall()
        con.close()
        return redirect(url_for("users"))
    else:
        return render_template('staffAddUser.html')

@app.route('/deleteUser/<usersID>', methods =["POST","GET"])
def deleteUser(usersID):
    con = sqlite3.connect('insurance.db')
    cur = con.cursor()
    usersData = cur.execute('select * from tbl_users')
    userData = usersData.fetchall()
    if request.method == "POST":
        F_name = request.form['userToDelete']
        cur.execute('delete from tbl_users where name = ?', (F_name, ))
        con.commit()
        usersData = cur.execute('select * from tbl_users')
        userData = usersData.fetchall()
        con.close()
        return redirect(url_for("users"))
    else:
        return render_template('staffDeleteUser.html', usersList = userData)
    
@app.route('/editUsers/<usersID>', methods =["POST","GET"])
def editUser(usersID):
    con = sqlite3.connect('insurance.db')
    cur = con.cursor()
    usersData = cur.execute('select * from tbl_users')
    userData = usersData.fetchall()
    if request.method == "POST":
        chosenUser = request.form['userToEdit']
        userToEditData = cur.execute('select * from tbl_users where name = ?', (chosenUser,))
        userToEdit = userToEditData.fetchone()
        
        name = userToEdit[1]
        username = userToEdit[2]
        password = userToEdit[3]
        userType = userToEdit[4]
        
        F_name = request.form['name']
        F_username = request.form['username']
        F_password = request.form['password']
        F_userType = request.form['staffType']
        
        if F_name != '':
            name = F_name
        if F_username != '':
            username = F_username
        if F_password != '':
            password = F_password
        if F_userType != '':
            userType = F_userType
        
                    
        cur.execute('update tbl_users set name = ?, username = ?, password = ?, userType = ? where name = ?',(name,username,password,userType,chosenUser))
        con.commit()
        usersData = cur.execute('select * from tbl_users')
        userData = usersData.fetchall()
        con.close()
        return redirect(url_for("users"))
    else:
        return render_template('staffEditUser.html', usersList = userData)
            
@app.route('/afterLoginCustomer/<usersID>', methods =["POST","GET"])
def afterLoginCustomer(usersID):
    con = sqlite3.connect('insurance.db')
    cur = con.cursor()
    allUsers = cur.execute('select * from tbl_users where userID = ?', (usersID,))
    users = allUsers.fetchone()
    policyData = cur.execute('select name,category,premium,policyID from tbl_policies')
    policiesData = policyData.fetchall()
    con.close()
    usersName = users[1]
    if request.method == "POST":
        choice = request.form['choice']
        if choice == "policies":
            return redirect(url_for("buyPolicies", usersID = users[0]))
        elif choice == "account":
            return redirect(url_for("viewUserDetails", usersID = users[0]))
        elif choice == "view":
            return redirect(url_for("viewUserPolicies", usersID = users[0]))
        else:
            return redirect(url_for("customerDeletePolicy", usersID = users[0]))
    else:
        return render_template('customerAfterLogin.html', name= usersName )
    
@app.route('/buyPolicies/<usersID>', methods =["POST","GET"])
def buyPolicies(usersID):
    con = sqlite3.connect('insurance.db')
    cur = con.cursor()
    policyData = cur.execute('select name,category,premium from tbl_policies')
    policiesData = policyData.fetchall()
    if request.method == "POST":
        policyName = request.form["policy"]
        startDate = request.form["date"]
        con.execute('insert into tbl_usersPolicies values(null,?,?,?)',(usersID,policyName,startDate))
        con.commit()
        usersPoliciesData = con.execute('select * from tbl_usersPolicies where userID = ?',(usersID,))
        usersPolicies = usersPoliciesData.fetchall()
        con.close()
        return redirect(url_for("viewUserPolicies", usersID = usersID))         
    else:
        return render_template('customerBuyPolicy.html', policies = policiesData)

@app.route('/cancelPolicies/<usersID>', methods =["POST","GET"])
def customerDeletePolicy(usersID):
    con = sqlite3.connect('insurance.db')
    cur = con.cursor()
    policyData = cur.execute('select * from tbl_usersPolicies where userID = ?', (usersID,))
    policiesData = policyData.fetchall()
    if request.method == "POST":
        policyName = request.form["policyToDelete"]
        con.execute('delete from tbl_usersPolicies where policyName = ? and userID = ?',(policyName,usersID))
        con.commit()
        usersPoliciesData = con.execute('select * from tbl_usersPolicies where userID = ?',(usersID,))
        usersPolicies = usersPoliciesData.fetchall()
        con.close()
        return redirect(url_for("viewUserPolicies", usersID = usersID))         
    else:
        return render_template('customerDeletePolicy.html', policies = policiesData)
    
@app.route('/viewPolicies/<usersID>', methods =["POST","GET"])
def viewUserPolicies(usersID):
    con = sqlite3.connect('insurance.db')
    cur = con.cursor()
    usersPoliciesData = con.execute('select * from tbl_usersPolicies where userID = ?',(usersID,))
    usersPolicies = usersPoliciesData.fetchall()
    con.close()
    return render_template('customerViewAll.html', policies = usersPolicies)
  
@app.route('/viewDetails/<usersID>', methods =["POST","GET"])
def viewUserDetails(usersID):
    con = sqlite3.connect('insurance.db')
    cur = con.cursor()
    usersData = con.execute('select * from tbl_users where userID = ?',(usersID,))
    users = usersData.fetchone()
    name = users[1]
    username = users[2]
    password = users[3]
    if request.method == "POST":
        F_name = request.form['name']
        F_username = request.form['username']
        F_password = request.form['Password']
        if F_name != '':
            name = F_name
        else:
            pass
        if F_username != '':
            username = F_username
        else:
            pass
        if F_password != '':
            password = F_password
        else:
            pass
        cur.execute('update tbl_users set name = ?, username = ?, password = ? where userID = ?',(name,username,password,usersID))
        con.close()
        return render_template('customerManage.html', name = name, username = username, password = password, msg = "Your details were updated as:")  
    else:
        return render_template('customerManage.html', name = name, username = username, password = password, msg = "Your details are:")  

@app.route('/register', methods =["POST","GET"])
def register():
    con = sqlite3.connect('insurance.db')
    cur = con.cursor()
    allUsers = cur.execute('select username from tbl_users')
    allUsersList = allUsers.fetchall()
    con.close()
    if request.method == "POST":
        pwd = request.form['Password']
        username = request.form['username']
        name = request.form['name']
        
        con = sqlite3.connect('insurance.db')
        cur = con.cursor()
        allUsers = cur.execute('select username from tbl_users')
        allUsersList = allUsers.fetchall()
        namesData = cur.execute('select username from tbl_users where username = ?', (username,))
        names = namesData.fetchone()
        if names is not None:
            return render_template('register.html', registerMessage = "Username is already taken, try again:")
        else:
            cur.execute('insert into tbl_users values(null,?,?,?,?)', (name,username,pwd,'C'))
            con.commit()
            con.close()
            return redirect(url_for("afterLoginCustomer"))        
        
    else:
        return render_template('register.html', registerMessage = "Please enter your details below:")

@app.route('/allPolicies')
def policies():
    con = sqlite3.connect('insurance.db')
    cur = con.cursor()
    policyData = cur.execute('select * from tbl_policies')
    policiesData = policyData.fetchall()
    con.close()
    return render_template('policies.html', policies = policiesData)

@app.route('/allUsers')
def users():
    con = sqlite3.connect('insurance.db')
    cur = con.cursor()
    userData = cur.execute('select * from tbl_users')
    usersData = userData.fetchall()
    con.close()
    return render_template('users.html', usersList = usersData)
    

@app.route('/viewPolicies')
def viewPolicies():
    con = sqlite3.connect('insurance.db')
    cur = con.cursor()
    policyData = cur.execute('select name,category,premium from tbl_policies')
    policiesData = policyData.fetchall()
    con.close()
    return render_template('viewPolicies.html', policies = policiesData)
app.run(debug=True)