from tqdm import tqdm

from algorithms.cpm import cpm


def rcpm(operations, df_resources):
    critical_path, _ = cpm(operations)

    # Проверка ресурсов
    machines = {res['type']: [0] for _, res in df_resources.iterrows()}
    
    for operation in tqdm(sorted(operations.values(), key=lambda op: op['early_start'])):
        operation_start_time = operation['early_start']
        
        # Конфликты
        while True:
            conflict = False
            for resource in operation['resources']:
                if resource in machines:
                    available_resources = machines[resource]

                    for release_time in available_resources:
                        if release_time > operation_start_time:
                            conflict = True
                            operation_start_time = release_time
                            break
                    if conflict:
                        break
            if not conflict:
                break

        for resource in operation['resources']:
            if resource in machines:
                available_resources = machines[resource]
                
                for i in range(len(available_resources)):
                    if available_resources[i] <= operation_start_time:
                        available_resources[i] = operation_start_time + operation['duration']
                        break
        
        delta = operation_start_time - operation['early_start']

        operation['early_start'] += delta
        operation['early_finish'] += delta
        operation['late_start'] += delta
        operation['late_finish'] += delta

    # Общая длительность
    total_duration = max(op['early_finish'] for op in operations.values())

    return critical_path, total_duration