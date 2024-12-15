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
        try:
            cursor = mysql.connection.cursor()
            with open('sql/create_table.sql', 'r') as f:
                sql = f.read()
            query = sql.split(';')
            for q in query:
                if q.strip():
                    cursor.execute(q.strip())
            mysql.connection.commit()
            print('table created')
        except Exception as e:
            print(f'create table error: {e}')
        finally:
            if cursor:
                cursor.close()

def stored_procedure():
    with app.app_context():
        try:
            cursor = mysql.connection.cursor()
            with open('sql/stored_procedure_setup.sql', 'r') as f:
                sql = f.read()
            cursor.execute(sql)
            mysql.connection.commit()
            print('stored procedure created')
        except Exception as e:
            print(f'stored procedure error: {e}')
        finally:
            if cursor:
                cursor.close()

@app.route('/', methods=['GET'])
def table():
    try:
        create_table()
        return 'table created'
    except Exception as e:
        return f'create table error: {e}'

@app.route('/procedure', methods=['GET'])
def procedure():
    try:
        stored_procedure()
        return 'stored procedure created', 200
    except Exception as e:
        return f'stored procedure error: {e}', 500

@app.route('/dummy', methods=['GET'])
def dummy():
    try:
        cursor = mysql.connection.cursor()
        cursor.callproc('InsertDummy')
        mysql.connection.commit()
        cursor.close()
        return 'dummy values inserted', 200
    except Exception as e:
        return f'insert error: {e}', 500

if __name__ == '__main__':
    app.run(debug=True)
