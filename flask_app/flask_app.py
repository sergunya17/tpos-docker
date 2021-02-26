#!/usr/bin/env python3

import json
from flask import Flask, Response
from sqlalchemy import create_engine, MetaData

app = Flask(__name__)
with open('/run/secrets/db_password', 'r') as file:
    password = file.read()
engine = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(
                        user='root', password=password, host='db', port=3306, database='db'))

@app.route('/', methods=['GET'])
def all_data():
    meta = MetaData()
    meta.reflect(engine)
    table = meta.sorted_tables[0]
    result = engine.connect().execute(table.select())
    result_json = json.dumps([dict(r) for r in result], indent=2) + '\n'
    return result_json

@app.route('/health', methods=['GET'])
def status():
    return Response("200\n", status=200)

@app.errorhandler(404)
def not_found(error):
    return Response("404\n", status=404)


app.run(debug=True, host='172.200.17.30', port=6767)
