import mysql.connector
def mySqlConnect():
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="notes_database"
  )
  return mydb

def make_tabs():
  mydb=mySqlConnect()
  mycursor = mydb.cursor()

  try:
    create_user="CREATE TABLE users(name varchar(20),email varchar(25) primary key,phone integer(10),pwd varchar(10)); "
    mycursor.execute(create_user)

    create_notes="CREATE TABLE notes(title varchar(20) primary key,content varchar(10000),created_date varchar(25),last_opened varchar(25),owner varchar(25),foreign key (owner) references users(email) On delete Cascade);"
    mycursor.execute(create_notes)
    print("Database is ready")
  except:
    print("Tables exist")

make_tabs()
