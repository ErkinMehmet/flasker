import mysql.connector

mydb=mysql.connector.connect(
    host="localhost",user="root",passwd="Fqm123!"
)
my_cursor=mydb.cursor()

my_cursor.execute("SHOW DATABASES")
exists=False
for db in my_cursor:
    print(db)
    if db[0]=='users':
        exists=True
if (not exists):
    my_cursor.execute("CREATE DATABASE users")