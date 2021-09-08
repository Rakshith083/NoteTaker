import mysql.connector
def mySqlConnect():
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="MyDb"
  )
  return mydb