import psycopg2
import pandas as pd

from config.database_config import host, user, password, dbname, port

from database_acts.create import create_init_database, create_results_table
from database_acts.delete import drop_table, drop_all_tables
from database_acts.insert import insert_resources, insert_operations, insert_add_info, insert_operations_from_csv, insert_resources_from_csv, insert_results_to_table
from database_acts.utils import export_table_to_csv

from algorithms.cpm import cpm
from algorithms.utils import prepare_operations, check_resource_conflicts, check_precedence_relations
from algorithms.rcpm import rcpm
from algorithms.ssgs import ssgs
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

if __name__ == "__main__":
    conn = connect_db()
    cur = conn.cursor()

    act = input("Выберите действие: create_init_tables, drop_table, drop_all_table, insert_csv, insert_manual, calculate_cpm, calculate_rcpm, calculate_ssgs, export_table_to_csv: ")


    if act == "create_init_tables":
        create_init_database(cur)
    elif act == "drop_table":
        drop_table(cur)
    elif act == "drop_all_table":
        drop_all_tables(cur)
    elif act == "insert_csv":
        insert_operations_from_csv(cur, r'data\operations.csv')
        insert_resources_from_csv(cur, r'data\resources.csv')  
    elif act == "insert_manual":
        insert_operations(cur)
        insert_resources(cur)
        insert_add_info(cur)

    elif act == "calculate_cpm":
        df_operations = pd.read_sql("SELECT * FROM operations", conn)
        operations = prepare_operations(df_operations)

        critical_path, total_duration = cpm(operations)
        print("Critical Path:", critical_path)
        print("RCPM Total Duration of the Project:", total_duration)
        plot_gantt_chart(operations)
        create_results_table(cur)
        insert_results_to_table(cur, operations)

    elif act == "calculate_rcpm":
        df_operations = pd.read_sql("SELECT * FROM operations", conn)
        df_resources = pd.read_sql("SELECT * FROM resources", conn)
        operations = prepare_operations(df_operations)

        critical_path, total_duration = rcpm(operations, df_resources)
        print("Critical Path:", critical_path)
        print("RCPM Total Duration of the Project:", total_duration)
        # plot_gantt_chart(operations)
        check_resource_conflicts(operations, df_resources)
        check_precedence_relations(operations)
        plot_gantt_and_resource_chart(operations, df_resources)
        create_results_table(cur)
        insert_results_to_table(cur, operations)

    elif act == "export_table_to_csv":
        export_table_to_csv(conn, 'results', 'results_output.csv')

    elif act == "calculate_ssgs":
        df_operations = pd.read_sql("SELECT * FROM operations", conn)
        df_resources = pd.read_sql("SELECT * FROM resources", conn)
        operations = prepare_operations(df_operations)

        critical_path, total_duration = ssgs(operations, df_resources, use_lft=False)
        check_resource_conflicts(operations, df_resources)
        check_precedence_relations(operations)
        plot_gantt_and_resource_chart(operations, df_resources)
        create_results_table(cur)
        insert_results_to_table(cur, operations)
    
    else:
        print("Такого действия нет!")

    cur.close()
    conn.close()