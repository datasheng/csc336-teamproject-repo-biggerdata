from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'MY_HOST'
app.config['MYSQL_USER'] = 'MY_USER'
app.config['MYSQL_PASSWORD'] = 'MY_PASSWORD'
app.config['MYSQL_DB'] = 'MY_DB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS account (name VARCHAR(20) NOT NULL, password VARCHAR(20) NOT NULL, PRIMARY KEY (name))') 
    cur.execute('INSERT INTO account VALUES ("name", "password")')
    cur.execute('SELECT * FROM account WHERE name = "name"')
    account = cur.fetchone()
    cur.close()
    return str(account)

if __name__ == '__main__':
    app.run(debug=True)
