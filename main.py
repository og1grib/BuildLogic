import psycopg2
import pandas as pd

from utils.createbd import create_database
from utils.config import host, user, password, dbname, port
from utils.insert_data import insert_resources, insert_operations, insert_operations_from_csv, insert_resources_from_csv
from algorithms.critical_path import compute_critical_path
from algorithms.utils import prepare_operations

conn = psycopg2.connect(
    host=host, 
    dbname=dbname, 
    user=user,
    password=password, 
    port=port
)

conn.autocommit = True
cur = conn.cursor()

# create_database(cur) # Создать 3 таблицы в БД

# insert_operations_from_csv(cur, 'operations.csv') # Из файла csv операции
# insert_resources_from_csv(cur, 'resources.csv') # Из файла csv ресурсы

# insert_operations(cur) # Ввод с клавиатуры операции
# insert_resources(cur) # Ввод с клавиатуры ресурсы

# Критический путь
query = """SELECT * FROM operations"""
df_oper = pd.read_sql(query, conn)

operations = prepare_operations(df_oper)
critical_path = compute_critical_path(operations)
print("Critical Path:", critical_path)

cur.close()
conn.close()
