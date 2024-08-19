from psycopg2.extras import execute_values
from psycopg2.extensions import register_adapter, AsIs

import pandas as pd
import numpy as np

register_adapter(np.int64, AsIs)
register_adapter(np.int32, AsIs)
register_adapter(np.float64, AsIs)
register_adapter(np.float32, AsIs)

# Из файла csv
def insert_operations_from_csv(cur, csv_file) -> None:
    df = pd.read_csv(csv_file)
        
    records = df.to_records(index=False)
    values = [tuple(record) for record in records]

    query = """INSERT INTO operations (op_id, duration, priority, release_time, predecessors, successors, resources) VALUES %s"""
    
    execute_values(cur, query, values)
    print(f"Данные из файла {csv_file} успешно загружены в таблицу operations.")


def insert_resources_from_csv(cur, csv_file) -> None:
    df = pd.read_csv(csv_file)
    
    records = df.to_records(index=False)
    values = [tuple(record) for record in records]

    query = """INSERT INTO resources (type, quantity) VALUES %s"""
    
    execute_values(cur, query, values)
    print(f"Данные из файла {csv_file} успешно загружены в таблицу resources.")

# Ручной ввод
def insert_resources(cur) -> None:
    resources_data = []

    while True:
        resource_type = input("Enter resource type (or 'q' to quit): ")
        if resource_type.lower() == 'q':
            break

        quantity = int(input("Enter quantity: ")) 
        resources_data.append((resource_type, quantity))
    
    if resources_data:
        query = """INSERT INTO resources (type, quantity) VALUES %s """
        execute_values(cur, query, resources_data)
    
    print(f"Введенные данные успешно загружены в таблицу resources.")



def insert_operations(cur):
    operations_data = []

    while True:
        op_id = input("Enter operation ID (or 'q' to quit): ")
        if op_id.lower() == 'q':
            break

        duration = int(input("Enter duration: "))
        priority = int(input("Enter priority: "))
        release_time = int(input("Enter release time: "))
        predecessors = input("Enter predecessors: ")
        successors = input("Enter successors: ")
        resources = input("Enter resources: ")
        deadline = input("Enter deadline: ")
        
        if deadline.lower() == 'none':
            deadline = None
        
        operations_data.append((op_id, duration, priority, release_time, predecessors, successors, resources, deadline))
    
    if operations_data:
        query = """INSERT INTO operations (op_id, duration, priority, release_time, predecessors, successors, resources, deadline) VALUES %s"""
        execute_values(cur, query, operations_data)

    print(f"Введенные данные успешно загружены в таблицу operations.")
    


def insert_add_info(cur) -> None:
    info_data = []

    while True:
        info_id = input("Enter info ID (or 'q' to quit): ")
        if info_id.lower() == 'q':
            break

        description = int(input("Enter description: ")) 
        info_data.append((info_id, description))
    
    if info_data:
        query = """INSERT INTO additional_info (info_id, description) VALUES %s """
        execute_values(cur, query, info_data)

    print(f"Введенные данные успешно загружены в таблицу additional_info.")


def insert_results_to_table(cur, operations) -> None:

    cur.execute("DELETE FROM results") # Очистка таблицы результатов 
    
    for op_id, op in operations.items():
        cur.execute(f"""INSERT INTO results (op_id, duration, predecessors, successors, resources, early_start, early_finish, late_start, late_finish, is_critical) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
            (op_id,
            op['duration'],
            str(list(op['predecessors'])),
            str(list(op['successors'])),
            str(op['resources']),
            op['early_start'],
            op['early_finish'],
            op['late_start'],
            op['late_finish'],
            op['is_critical'])
            )
        
    print(f"Результаты успешно сохранены в таблице results.")