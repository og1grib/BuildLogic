import psycopg2
import pandas as pd

from config.database_config import host, user, password, dbname, port

from database_acts.create import create_database
from database_acts.delete import drop_table

from database_acts.insert import insert_resources, insert_operations, insert_add_info, insert_operations_from_csv, insert_resources_from_csv
from algorithms.cpm import cpm
from algorithms.utils import prepare_operations, check_resource_conflicts
from algorithms.rcpm import rcpm
from plot.gantt_chart import plot_gantt_chart, plot_gantt_and_resource_chart

def connect_db():
    conn = psycopg2.connect(
        host=host, 
        dbname=dbname, 
        user=user,
        password=password, 
        port=port
    )
    conn.autocommit = True
    return conn

def create_tables(cur):
    create_database(cur)

def drop_tables(cur):
    drop_table(cur)

def insert_data_from_csv(cur):
    insert_operations_from_csv(cur, r'data\operations.csv')
    insert_resources_from_csv(cur, r'data\resources.csv')     

def insert_data_manually(cur):
    insert_operations(cur)
    insert_resources(cur)
    insert_add_info(cur)

def calculate_cpm():
    df_operations = pd.read_sql("SELECT * FROM operations", conn)
    operations = prepare_operations(df_operations)

    critical_path, total_duration = cpm(operations)
    print("Critical Path:", critical_path)
    print("RCPM Total Duration of the Project:", total_duration)
    plot_gantt_chart(operations)

def calculate_rcpm():
    df_operations = pd.read_sql("SELECT * FROM operations", conn)
    df_resources = pd.read_sql("SELECT * FROM resources", conn)
    operations = prepare_operations(df_operations)

    critical_path, total_duration = rcpm(operations, df_resources)
    print("Critical Path:", critical_path)
    print("RCPM Total Duration of the Project:", total_duration)
    # plot_gantt_chart(operations)
    check_resource_conflicts(operations, df_resources)
    plot_gantt_and_resource_chart(operations, df_resources)


if __name__ == "__main__":
    conn = connect_db()
    cur = conn.cursor()

    action = input("Выберите действие: create, drop, insert_csv, insert_manual, calculate_cpm, calculate_rcpm: ")


    if action == "create":
        create_tables(cur)
    elif action == "drop":
        drop_tables(cur)
    elif action == "insert_csv":
        insert_data_from_csv(cur)
    elif action == "insert_manual":
        insert_data_manually(cur)
    elif action == "calculate_cpm":
        calculate_cpm()
    elif action == "calculate_rcpm":
        calculate_rcpm()
        
    else:
        print("Такого действия нет!")

    cur.close()
    conn.close()





# create_database(cur) # Создать таблицы в БД

# insert_operations_from_csv(cur, r'data\operations.csv') # Из файла csv операции
# insert_resources_from_csv(cur, r'data\resources.csv') # Из файла csv ресурсы

# # insert_operations(cur) # Ввод с клавиатуры операции
# # insert_resources(cur) # Ввод с клавиатуры ресурсы
# # insert_add_info(cur) # Ввод с клавиатуры доп инфу

# # # Критический путь
# df_operations = pd.read_sql("SELECT * FROM operations", conn)
# df_resources = pd.read_sql("SELECT * FROM resources", conn)

# operations = prepare_operations(df_operations)
# # critical_path, total_duration = cpm(operations)


# # Критический путь с проверкой на ресурсы
# critical_path, total_duration = rcpm(operations, df_resources)

# print("Critical Path:", critical_path)
# print("RCPM Total Duration of the Project:", total_duration)

# plot_gantt_chart(operations)

# # drop_table(cur)

# cur.close()
# conn.close()