from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MY_HOST')
app.config['MYSQL_USER'] = os.getenv('MY_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MY_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MY_DB')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def create_table():
    with app.app_context():
        cursor = mysql.connection.cursor()
        try:
            path = 'create_table.sql'
            with open(path, 'r') as f:
                script = f.read()
            query = script.split(';')
            for q in query:
                if q.strip():
                    cursor.execute(q.strip())
                    mysql.connection.commit()
            cursor.close()
            print('table created')
        except Exception as e:
            print(f'create table error: {e}')

def stored_procedure():
    with app.app_context():
        cursor = mysql.connection.cursor()
        try:
            path = 'stored_procedure.sql'
            with open(path, 'r') as f:
                script = f.read()
            cursor.execute(script)
            mysql.connection.commit()
            cursor.close()
            print('stored procedure created')
        except Exception as e:
            print(f'stored procedure error: {e}')

@app.route('/procedure', methods=['GET'])
def procedure():
    try:
        stored_procedure()
        return 'stored procedure created'
    except Exception as e:
        return f'stored procedure error: {e}'

@app.route('/dummy', methods=['GET'])
def dummy():
    try:
        cursor = mysql.connection.cursor()
        cursor.callproc('InsertDummy')
        mysql.connection.commit()
        cursor.close()
        return 'dummy values inserted'
    except Exception as e:
        return f'insert error: {e}'

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
