import matplotlib.pyplot as plt
import pandas as pd

# Диаграмма Ганта
def plot_gantt_chart(operations):
    gant_data = []
    
    for op_id, operation in operations.items():
        gant_data.append({
            'Task': op_id,
            'Start': operation['early_start'],
            'Finish': operation['early_finish'],
            'Critical': operation.get('is_critical', False)
        })

    df_gant = pd.DataFrame(gant_data)

    plt.figure(figsize=(10, 6))

    for _, row in df_gant.iterrows():
        color = 'red' if row['Critical'] else 'blue'
        plt.barh(row['Task'], row['Finish'] - row['Start'], left=row['Start'], color=color)

    plt.xlabel('Time')
    plt.ylabel('Tasks')
    plt.title('Gantt Chart')
    plt.show()