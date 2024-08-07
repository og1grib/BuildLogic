from psycopg2.extras import execute_values
import json
import pandas as pd
import numpy as np
from psycopg2.extensions import register_adapter, AsIs


register_adapter(np.int64, AsIs)
register_adapter(np.int32, AsIs)
register_adapter(np.float64, AsIs)
register_adapter(np.float32, AsIs)


# Из файла csv
def insert_operations_from_csv(cur, csv_file):
    df = pd.read_csv(csv_file)
        
    records = df.to_records(index=False)
    values = [tuple(record) for record in records]

    query = """INSERT INTO operations (op_id, duration, priority, release_time, predecessors, successors, resources) VALUES %s"""
    
    execute_values(cur, query, values)


def insert_resources_from_csv(cur, csv_file):
    df = pd.read_csv(csv_file)
    
    # df['resource'] = df['resource'].apply(lambda x: json.dumps(eval(x)))
    records = df.to_records(index=False)
    values = [tuple(record) for record in records]

    query = """INSERT INTO resources (type, quantity) VALUES %s"""
    
    execute_values(cur, query, values)


# Ручной ввод
def insert_resources(cur):
    resources_data = []

    while True:
        resource_type = input("Enter resource type (or 'q' to quit): ")
        if resource_type.lower() == 'q':
            break

        # resource_key = input("Enter resource key: ")
        # resource_value = int(input("Enter resource value: "))
        
        # resource_json = json.dumps({resource_key: resource_value})
        # resources_data.append((resource_type, resource_json))

        quantity = int(input("Enter quantity: ")) 
        resources_data.append((resource_type, quantity))
    
    if resources_data:
        query = """INSERT INTO resources (type, quantity) VALUES %s """
        execute_values(cur, query, resources_data)


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


def insert_add_info(cur):
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