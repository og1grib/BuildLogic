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

def calculate_cpm(cur, df_operations):
    operations = prepare_operations(df_operations) # Словарь из operations

    critical_path, total_duration = cpm(operations)
    print("Critical Path:", critical_path)
    print("CPM Total Duration of the Project:", total_duration)
    # plot_gantt_chart(operations)
    insert_results_to_table(cur, operations)

def calculate_rcpm(cur, df_operations, df_resources):
    operations = prepare_operations(df_operations)

    critical_path, total_duration = rcpm(operations, df_resources)
    print("Critical Path:", critical_path)
    print("RCPM Total Duration of the Project:", total_duration)

    check_resource_conflicts(operations, df_resources) # Проверка конфликт ресурсов
    check_precedence_relations(operations) # Проверка конфликт предшествоания
    # plot_gantt_and_resource_chart(operations, df_resources)

    insert_results_to_table(cur, operations)

def calculate_ssgs(cur, df_operations, df_resources):
    operations = prepare_operations(df_operations)

    critical_path, total_duration = ssgs(operations, df_resources)
    print("Critical Path:", critical_path)
    print("SSGS Total Duration of the Project:", total_duration)

    check_resource_conflicts(operations, df_resources)
    check_precedence_relations(operations)
    # plot_gantt_and_resource_chart(operations, df_resources)

    insert_results_to_table(cur, operations)

def calculate_rcpm_with_local_sgs(cur, df_operations, df_resources, selected_tasks, use_pr=False):
    operations = prepare_operations(df_operations)

    critical_path, total_duration = rcpm(operations, df_resources)
    total_duration = local_ssgs(operations, df_resources, selected_tasks, use_pr=use_pr)

    print("Critical Path:", critical_path)
    print("RCPM with local SSGS Total Duration of the Project:", total_duration)

    check_resource_conflicts(operations, df_resources)
    check_precedence_relations(operations)
    # plot_gantt_and_resource_chart(operations, df_resources)

    insert_results_to_table(cur, operations)

if __name__ == "__main__":
    conn = connect_db()
    cur = conn.cursor()

    act = input("Выберите действие: create_tables, drop_table, drop_all_tables, insert_csv, insert_manual, calculate_cpm, calculate_rcpm, calculate_ssgs, calculate_rcpm_with_local_sgs, export_table_to_csv: ")
    df_operations = pd.read_sql("SELECT * FROM operations", conn)
    df_resources = pd.read_sql("SELECT * FROM resources", conn)
    selected_tasks = [
                            # "TASK1/_/1",
                            # "TASK1/_/2",
                            # "TASK1/_/3",
                            "TASK2/_/4",
                            "TASK1/_/5",
                            "TASK2/_/6",
                            "TASK3/_/7",
                            "TASK3/_/8",
                            "TASK3/_/9",
                            "TASK4/_/10",
                            "TASK4/_/11",
                            "TASK4/_/12",
                            # "TASK4/_/13",
                            # "TASK4/_/14",
                            # "TASK4/_/15"
                        ]

    if act == "create_tables":
        create_tables(cur)
    elif act == "drop_table":
        drop_table(cur, "results")
    elif act == "drop_all_tables":
        drop_all_tables(cur)
    elif act == "insert_csv":
        insert_operations_from_csv(cur, 'data/operations.csv')
        insert_resources_from_csv(cur, 'data/resources.csv')  
    elif act == "insert_manual":
        insert_operations(cur)
        insert_resources(cur)
        insert_add_info(cur)

    elif act == "calculate_cpm":
        calculate_cpm(cur, df_operations)

    elif act == "calculate_rcpm":
        calculate_rcpm(cur, df_operations, df_resources)

    elif act == "calculate_ssgs":
        calculate_ssgs(cur, df_operations, df_resources)

    elif act == "calculate_rcpm_with_local_sgs":
        calculate_rcpm_with_local_sgs(cur, df_operations, df_resources, selected_tasks)
        
    elif act == "export_results_to_csv":
        export_table_to_csv(conn, 'results', 'results_output.csv')
    
    else:
        print("Такого действия нет!")

    cur.close()
    conn.close()