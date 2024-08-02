import psycopg2
import pandas as pd

from utils.createbd import create_database
from utils.config import host, user, password, dbname, port
from utils.insert_data import insert_resources, insert_operations, insert_operations_from_csv, insert_resources_from_csv
from algorithms.cpm import cpm
from algorithms.utils import prepare_operations
from algorithms.rcpm import rcpm

conn = psycopg2.connect(
    host=host, 
    dbname=dbname, 
    user=user,
    password=password, 
    port=port
)

conn.autocommit = True
cur = conn.cursor()

# create_database(cur) # Создать таблицы в БД

# insert_operations_from_csv(cur, r'data\operations.csv') # Из файла csv операции
# insert_resources_from_csv(cur, r'data\resources.csv') # Из файла csv ресурсы

# insert_operations(cur) # Ввод с клавиатуры операции
# insert_resources(cur) # Ввод с клавиатуры ресурсы

# Критический путь
df_operations = pd.read_sql("SELECT * FROM operations", conn)
df_resources = pd.read_sql("SELECT * FROM resources", conn)

operations = prepare_operations(df_operations)
# critical_path, total_duration = cpm(operations)

# Критический путь с проверкой на ресурсы
critical_path, total_duration = rcpm(operations, df_resources)

print("Critical Path:", critical_path)
print("Total Duration of the Project:", total_duration)


cur.close()
conn.close()