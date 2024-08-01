import psycopg2

from utils.createbd import create_database
from utils.config import host, user, password, dbname, port
from utils.insert_data import insert_resources, insert_operations, insert_operations_from_csv, insert_resources_from_csv

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

cur.close()
conn.close()
    
