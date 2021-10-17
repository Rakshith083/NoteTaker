from flask import *
from mycon import mySqlConnect
import datetime
from random import *

app = Flask(__name__)
@app.route('/signup' ,methods=['get','post'])
def signup():
    if request.method == "GET":
        return render_template("regi.html")
    else:
        name=request.form['name']
        mail=request.form['mail']
        try:
            phn=int(request.form['phone'])
        except:
            msg='worst contact number!!'
            alert='alert-danger'
            return render_template('regi.html',msg=msg,alert=alert)
        pas=request.form['pas']

        mydb = mySqlConnect()
        mycursor = mydb.cursor()
        
        try:
            sql = "INSERT INTO users (name,email,phone,pwd) VALUES (%s,%s,%s,%s)"
            val = (name, mail,phn,pas)
            mycursor.execute(sql, val)
            mydb.commit()
            #print(mycursor.rowcount, "record inserted.")
            msg='Account created !'
            alert='alert-success'
            return render_template('login.html',msg=msg,alert=alert)
        except:
            msg='user already exist !!'
            alert='alert-danger'
            return render_template('regi.html',msg=msg,alert=alert)

info=[]

@app.route('/' ,methods=['get','post'])
def login():
    info.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        mail=request.form['mail']
        pas=request.form['pas']

        mydb = mySqlConnect()
        mycursor = mydb.cursor()
        sql="SELECT pwd FROM users where email=%s"
        mycursor.execute(sql,(mail,))
        myresult = mycursor.fetchall()
        print(myresult[0][0])
        if(myresult[0][0] == pas):
            info.append(mail)
            return redirect('/allNotes')
        else:
            alert="alert-danger"
            msg="Invalid credencials!"
            return render_template("login.html",alert=alert,msg=msg)

@app.route('/save' ,methods=['get','post'])
def save():
    if request.method == "GET":
        return render_template("newNote.html")
    else:
        title=request.form["title"]
        content=request.form["note"]
        created = str(datetime.datetime.now())[0:19]
        lastOpen=created
        mail=info[0]

        try:
            mydb = mySqlConnect()
            mycursor = mydb.cursor()
            sql="insert into notes(title,content,created_date,last_opened,owner) values(%s,%s,%s,%s,%s)"
            val=(title,content,created,lastOpen,mail)
            mycursor.execute(sql,val)
            mydb.commit()
            msg="Note Saved"
            alert="alert-success"
            return redirect('/allNotes') #render_template('newNote.html',content=content,alert=alert,msg=msg)
        except:
            msg="Unable to save , Title already exists!!"
            alert="alert-danger"
            return render_template('newNote.html',content=content,alert=alert,msg=msg)

@app.route('/allNotes')
def allnotes():
    mydb = mySqlConnect()
    mycursor = mydb.cursor()

    sql1="SELECT count(*) FROM notes n,users u where n.owner=%s and u.email=%s "
    mycursor.execute(sql1,(info[0],info[0],))
    myresult1 = mycursor.fetchall()
    cnt=myresult1[0][0]
    print(cnt)

    sql="SELECT title,created_date,last_opened FROM notes,users where owner=%s and email=%s"
    mycursor.execute(sql,(info[0],info[0],))
    myresult = mycursor.fetchall()
    print(myresult)
    msg=str(cnt)+" note(s) found"
    return render_template('notes.html',notes=myresult,msg=msg)

@app.route('/delete/<title>')
def delete(title):
    mydb = mySqlConnect()
    mycursor = mydb.cursor()
    sql="DELETE FROM notes WHERE title=%s"
    mycursor.execute(sql,(title,))
    mydb.commit()
    return redirect('/allNotes')

titleList=[]

@app.route('/view/<title>' ,methods=['get'])
def view(title):
    titleList.append(title)
    mydb = mySqlConnect()
    mycursor = mydb.cursor()

    sql="SELECT content FROM notes n,users u WHERE title=%s and n.owner=%s and u.email=%s"
    mycursor.execute(sql,(title,info[0],info[0],))
    myresult = mycursor.fetchall()
        
    last_time=str(datetime.datetime.now())[0:19]
    sql2="UPDATE notes SET last_opened = %s WHERE title = %s"
    mycursor.execute(sql2,(last_time,title))
    mydb.commit()
    return render_template('viewUpdate.html',content=myresult[0][0],title=title)
    
@app.route('/viewOne' ,methods=['POST'])
def update():
    content=request.form['note']
    mydb = mySqlConnect()
    mycursor = mydb.cursor()
    last_time=str(datetime.datetime.now())[0:19]
    sql2="UPDATE notes SET content=%s, last_opened = %s WHERE title = %s"
    mycursor.execute(sql2,(content,last_time,titleList[0],))
    mydb.commit()
    titleList.clear()
    return redirect('/allNotes')

if __name__ == "__main__":
    app.run(debug=True)
