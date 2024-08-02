import ast

def prepare_operations(df):
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
