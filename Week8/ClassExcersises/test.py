from flask import Flask, jsonify, abort, request
import pymysql
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World from flask server!"

@app.route('/datagenerator/api/person/<int:no>', methods=['GET'])
def get_person(no):
    cnx = pymysql.connect(user='dev', password='ax2',host='127.0.0.1',port=3306,db='test')
    with cnx.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('SELECT id, name FROM person')
        data = cursor.fetchall()
    cnx.close()
    return jsonify({'persons': data})

@app.route('/datagenerator/api/person', methods=['POST'])
def create_task():
    cnx = pymysql.connect(user='dev', password='ax2',host='127.0.0.1',port=3306,db='test')
    with cnx.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('SELECT id, name FROM person')
        data = cursor.fetchall()

        if not request.json or not 'name' in request.json:
            abort(400)
        person = {
            'id': data[-1]['id'] + 1,
            'name': request.json['name']
        }
        cursor.execute('INSERT INTO person VALUES (%(id)s, %(name)s)', (person))
        cnx.commit()
    cnx.close()
    return jsonify({'person': person}), 201

if __name__ == '__main__':
    app.run(debug=True)