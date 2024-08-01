


def prepare_operations(df):
    operations = {}
    for _, row in df.iterrows():
        operations[row['op_id']] = {
            'duration': row['duration'],
            'predecessors': eval(row['predecessors']),
            'successors': eval(row['successors']),
            'early_start': 0,
            'early_finish': 0,
            'late_start': 0,
            'late_finish': 0,
            'is_critical': False
        }
    return operations
