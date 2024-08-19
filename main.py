import psycopg2
import pandas as pd

from config.database_config import host, user, password, dbname, port

from src.database import *
from src.algorithms import *
from src.plot import * 


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

if __name__ == "__main__":
    conn = connect_db()
    cur = conn.cursor()

    act = input("Выберите действие: create_tables, drop_table, drop_all_table, insert_csv, insert_manual, calculate_cpm, calculate_rcpm, calculate_ssgs, export_table_to_csv: ")

    if act == "create_tables":
        create_tables(cur)
    elif act == "drop_table":
        drop_table(cur, "results")
    elif act == "drop_all_table":
        drop_all_tables(cur)
    elif act == "insert_csv":
        insert_operations_from_csv(cur, 'data/operations.csv')
        insert_resources_from_csv(cur, 'data/resources.csv')  
    elif act == "insert_manual":
        insert_operations(cur)
        insert_resources(cur)
        insert_add_info(cur)

    elif act == "calculate_cpm":
        df_operations = pd.read_sql("SELECT * FROM operations", conn)
        operations = prepare_operations(df_operations) # Словарь из operations

        critical_path, total_duration = cpm(operations)
        print("Critical Path:", critical_path)
        print("CPM Total Duration of the Project:", total_duration)
        plot_gantt_chart(operations)
        insert_results_to_table(cur, operations)

    elif act == "calculate_rcpm":
        df_operations = pd.read_sql("SELECT * FROM operations", conn)
        df_resources = pd.read_sql("SELECT * FROM resources", conn)
        operations = prepare_operations(df_operations)

        critical_path, total_duration = rcpm(operations, df_resources)
        print("Critical Path:", critical_path)
        print("RCPM Total Duration of the Project:", total_duration)

        check_resource_conflicts(operations, df_resources) # Проверка конфликт ресурсов
        check_precedence_relations(operations) # Проверка конфликт предшествоания
        plot_gantt_and_resource_chart(operations, df_resources)

        insert_results_to_table(cur, operations)

    elif act == "calculate_ssgs":
        df_operations = pd.read_sql("SELECT * FROM operations", conn)
        df_resources = pd.read_sql("SELECT * FROM resources", conn)
        operations = prepare_operations(df_operations)

        critical_path, total_duration = ssgs(operations, df_resources)
        print("Critical Path:", critical_path)
        print("SSGS Total Duration of the Project:", total_duration)

        check_resource_conflicts(operations, df_resources)
        check_precedence_relations(operations)
        plot_gantt_and_resource_chart(operations, df_resources)

        insert_results_to_table(cur, operations)

    elif act == "export_results_to_csv":
        export_table_to_csv(conn, 'results', 'results_output.csv')
    
    else:
        print("Такого действия нет!")

    cur.close()
    conn.close()