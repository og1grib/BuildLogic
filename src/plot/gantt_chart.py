import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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


def plot_gantt_and_resource_chart(operations, resources):
    schedule = {op_id: op['early_start'] for op_id, op in operations.items()}
    act_proc = {op_id: op['duration'] for op_id, op in operations.items()}
    
    r_cap = {row['type']: row['quantity'] for _, row in resources.iterrows()}
    
    finish_times = {act: schedule[act] + act_proc[act] for act in schedule}
    total_time = max(finish_times.values())

    _, axs = plt.subplots(2, 1, figsize=(15, 10), gridspec_kw={'height_ratios': [3, 1]})
    
    gant_data = []

    for act, start_time in schedule.items():
        duration = act_proc[act]
        color = 'red' if operations[act].get('is_critical', False) else 'blue'
        axs[0].barh(act, duration, left=start_time, color=color, edgecolor='black')
        gant_data.append({
            'Task': act,
            'Start': start_time,
            'Finish': start_time + duration,
            'Critical': operations[act].get('is_critical', False)
        })

    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Tasks')
    axs[0].set_title('Gantt Chart (with resources)')
    
    axs[0].set_xlim(0, total_time)
    axs[1].set_xlim(0, total_time)
    
    resource_usage = {r: np.zeros(total_time + 1) for r in r_cap}
    for act in schedule:
        start = schedule[act]
        end = start + act_proc[act]
        for r in operations[act]['resources']:
            resource_usage[r][start:end] += 1

    legend_handles = [] 
    for idx, (r, usage) in enumerate(resource_usage.items()):
        line, = axs[1].plot(usage, drawstyle='steps-post', label=f'Resource {r}')
        axs[1].axhline(y=r_cap[r], linestyle='--', linewidth=1) 
        legend_handles.append(line)

    axs[1].set_ylim(0, max(r_cap.values()) + 1)
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Resource Utilization')
    # axs[1].set_title('Resource Utilization Over Time')
    
    axs[1].legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    
    axs[1].grid(True)

    plt.tight_layout()
    plt.subplots_adjust(right=0.85)
    plt.show()