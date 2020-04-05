from flask import Flask, jsonify
import pymysql

app = Flask(__name__)
cnx = pymysql.connect(user='dev', password='ax2', host='127.0.0.1', port=3306, db='test')

@app.route('/')
def get_index():
    return '<ul><li>/api/whois/all</li><li>/api/whois/string:id</li></ul>'

@app.route('/api/whois/<string:ip>')
def get_single(ip):
    query = 'SELECT * FROM whois WHERE ip = %s'
    with cnx.cursor() as cursor:
        cursor.execute(query, ip)
        return jsonify(cursor.fetchall())

@app.route('/api/whois/all')
def get_all():
    query = 'SELECT * FROM whois'
    with cnx.cursor() as cursor:
        cursor.execute(query)
        return jsonify(cursor.fetchall())
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)