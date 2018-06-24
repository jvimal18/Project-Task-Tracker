'''
Created on Jun 21, 2018

@author: Vimal Jay
'''

from flask import Flask, render_template, request, session, flash, redirect, \
    url_for, jsonify
from datetime import timedelta, datetime
from common.database import Database
from models.Task import Task
from models.users import User

app = Flask(__name__)

app.debug = True
app.secret_key = 'vimal'


@app.before_first_request
def initializedb():
    Database.initialize()
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


#Login Page

@app.route('/' , methods= ['POST', 'GET'])               
@app.route('/login', methods= ['POST', 'GET'])
@app.route('/login/<string:message>', methods= ['GET', 'POST'])
def login(message=None):
    if request.method == 'POST':  
        email = request.form['email']
        password = request.form['password']

        if User.loginvalid(email, password):
            if session['isadmin'] == "Admin":
                return redirect(url_for('admin'))
            elif session['isadmin'] == "Normal":
                return redirect(url_for('user'))
        else:  
            return render_template('login.html', message="Invalid credentials, if you dnt have account kind reach admin".format(email))
    else:
        return render_template('login.html', message=message)


# Admin Page URL
@app.route('/admin', methods= ['GET'])
@app.route('/admin/<string:message>', methods= ['GET'])
def admin(message=None):
    if request.method == "GET":
        if User.validatloginsession():
            tasklist = User.get_alltask()
            userlist = User.get_users('name')
            if session['isadmin'] == 'Admin':
                if message is not None:
                    return render_template("admin.html", task=tasklist, userlist=userlist, name=session['name'], Role=session['isadmin'], message=message)
                else:
                    return render_template("admin.html", task=tasklist, userlist=userlist, name=session['name'], Role=session['isadmin'])
            else:
                session['email'] = None
                return redirect( url_for('login', message="You Tried to access admin page, without admin access!!!"
                                                          "You have been logged out"))
        return redirect( url_for('login', message="!!!!!!Please login to access the page!!!!!!"))
    

# User Page URL
@app.route('/user', methods= ['GET'])
@app.route('/user/<string:message>', methods= ['GET'])
def user(message=None):
    if request.method == "GET":
        if User.validatloginsession():
            Alltasklist = User.get_alltask()
            usertasklist = User.gettaskbyname()               
            if message is not None:
                return render_template("user.html", task=Alltasklist, 
                                       usertasklist=usertasklist, name=session['name'], 
                                       Role=session['isadmin'], message=message)
            else:
                return render_template("user.html", task=Alltasklist, 
                                       usertasklist=usertasklist, name=session['name'], 
                                       Role=session['isadmin'])
        return redirect( url_for('login', message="!!!!!!Please login to access the page!!!!!!"))

 
@app.route('/addtask', methods= ['POST'])
def addtask():
    
    print(request.form)
    taskname = request.form['TaskName']
    owner = request.form['owner']
    summary = request.form['Summary']
    managedby = request.form['managedby']
    percent = request.form['percent']
    comments = request.form['comments']
    eta = request.form['eta']
    status =request.form['Status']
    task = Task(taskname, owner, summary, managedby, percent, comments, eta, status)
    task.save_to_db()
    message= "Task {} added to Database".format(taskname)
    
    if session['isadmin'] == "Admin":
        return redirect( url_for('admin', message=message))
    else:
        return redirect( url_for('user', message=message))
    

@app.route('/updatetask', methods= ['POST'])
def updatetask():
    taskname = request.form['taskname']
    formdata = request.form.to_dict()
    query = Task.remove_empty_from_dict(formdata)
    modifieddate=datetime.now().strftime("%Y-%m-%d")
    query.update({'modifieddate': modifieddate})
    print(query)

    Task.update_dbdoc(taskname, query)

    if session['isadmin'] == "Admin":
        return redirect( url_for('admin', message="{} Update successfully".format(taskname)))
    else:
        return redirect( url_for('user', message="{} Update successfully".format(taskname)))

      
@app.route('/adduser', methods= ['POST'])
def adduser():
        username = request.form['user']
        email = request.form['emailid']
        password = request.form['password']
        isadmin = request.form['admin']
        user = User(email, password, isadmin, username)
        user.create_user()
        message = "successfully added user {}".format(username)
        return redirect( url_for('admin', message=message))   


@app.route('/logout', methods= ['GET'])
def logout():
    session['email'] = None
    return redirect("login")


if __name__ == '__main__':
    app.run(port=1808)

