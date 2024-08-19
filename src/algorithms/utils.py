import ast
import numpy as np

def prepare_operations(df) -> dict:
    operations = {}

    for _, row in df.iterrows():
        operations[row['op_id']] = {
            'duration': row['duration'],
            'predecessors': ast.literal_eval(row['predecessors']),
            'successors': ast.literal_eval(row['successors']),
            'early_start': 0,
            'early_finish': 0,
            'late_start': 0,
            'late_finish': 0,
            'resources': ast.literal_eval(row['resources']),
            'is_critical': False
        }
    return operations

def generate_sequence_by_est(operations) -> list:
    est_copy = {op_id: op['early_start'] for op_id, op in operations.items()}
    all_activities = list(operations.keys())
    sequence_by_est = []

    while all_activities:
        min_est_activity = min(all_activities, key=lambda act: est_copy[act])
        sequence_by_est.append(min_est_activity)
        all_activities.remove(min_est_activity)
        del est_copy[min_est_activity]

    return sequence_by_est


def check_resource_conflicts(operations, df_resources) -> None:
    resources = {row['type']: row['quantity'] for _, row in df_resources.iterrows()}

    total_time = max(op['early_finish'] for op in operations.values())
    resource_usage = {r: np.zeros(total_time + 1) for r in resources.keys()}
    
    for act, op in operations.items():
        start = op['early_start']
        end = op['early_finish']
        for r in op['resources']:
            if r in resource_usage:
                resource_usage[r][start:end] += 1
            else:
                print(f"Ресурс {r} не найден.")

    conflicts = {r: [] for r in resources.keys()}
    for r, usage in resource_usage.items():
        for t in range(len(usage)):
            if usage[t] > resources[r]:
                conflicts[r].append(t)
    
    if all(not times for times in conflicts.values()):
        print("Нет конфликтов ресурсов.")
    else:
        for r, times in conflicts.items():
            if times:
                print(f"Конфликты с ресурсом {r} в моменты времени: {times}")


def check_precedence_relations(operations) -> None:
    errors = []
    
    for act_id, act in operations.items():
        for pred_id in act['predecessors']:
            if operations[pred_id]['early_finish'] > act['early_start']:
                errors.append(f"Операция {act_id} начинается раньше, чем заканчивается её предшественник {pred_id}.")

    if errors:
        print("Конфликты в предшестовании:")
        for error in errors:
            print(error)
    else:
        print("Нет конфликтов предешестования.")