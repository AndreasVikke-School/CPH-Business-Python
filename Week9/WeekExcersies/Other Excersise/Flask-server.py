from flask import Flask, jsonify
import pymysql

app = Flask(__name__)
cnx = pymysql.connect(user='dev', password='ax2', host='127.0.0.1', port=3306, db='test')


@app.route('/')
def get_index():
    return '<ul><li>/api/worldpop/all</li><li>/api/worldpop/string:id</li></ul>'

@app.route('/api/worldpop/<string:id>')
def get_single(id):
    query = 'SELECT * FROM worldpop WHERE counterId = %s'
    with cnx.cursor() as cursor:
        cursor.execute(query, id)
        return jsonify(cursor.fetchall())

@app.route('/api/worldpop/all')
def get_all():
    query = 'SELECT * FROM worldpop'
    with cnx.cursor() as cursor:
        cursor.execute(query)
        return jsonify(cursor.fetchall())
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)