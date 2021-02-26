#!/usr/bin/env python3

import pandas as pd
from sqlalchemy import create_engine, Table, MetaData, types
from glob import glob

TABLE_NAME = 'Table'
FIRST_COLUMN_NAME = 'text'
SECOND_COLUMN_NAME = 'number'

data_filename = glob('data/*.csv')[0]
try:
    data = pd.read_csv(data_filename, names=[FIRST_COLUMN_NAME, SECOND_COLUMN_NAME],
                       dtype={FIRST_COLUMN_NAME: 'object', SECOND_COLUMN_NAME: 'float64'})
except ValueError as e:
    try:
        data = pd.read_csv(data_filename, header=0)
        data.iloc[:, 0] = data.iloc[:, 0].astype('object')
        data.iloc[:, 1] = data.iloc[:, 1].astype('float64')
    except ValueError as e:
        print("Wrong data type")
        exit()

with open('/run/secrets/db_password', 'r') as file:
    password = file.read()
engine = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(
                        user='root', password=password, host='db', port=3306, database='db'))
meta = MetaData()
meta.reflect(engine)
meta.drop_all(engine)

data.to_sql(TABLE_NAME, engine, if_exists='replace', index=False,
            dtype={data.columns[0]: types.Text(), data.columns[1]: types.Float()})

table = Table(TABLE_NAME, MetaData(bind=None), autoload=True, autoload_with=engine)
with engine.connect() as connection:
    result = connection.execute(table.select()).fetchall()
print('Successfully filled lines:', len(result))
