from algorithms.cpm import cpm
from algorithms.utils import generate_sequence_by_est

def ssgs(operations, resources, use_lft=False):
    critical_path, _ = cpm(operations)
    schedule_start_times = {}
    scheduled_activities = []

    # Основной цикл для планирования операций
    for _ in range(len(operations)):
        eligible_activities = [
            act_id for act_id, act_data in operations.items()
            if act_id not in scheduled_activities and all(pred in scheduled_activities for pred in act_data['predecessors'])
        ]

        if not eligible_activities:
            print('Не удалось создать корректное расписание.')
            break

        # Используем правило приоритета для выбора операции
        if use_lft:
            selected_activity = min(eligible_activities, key=lambda x: operations[x]['late_finish'])
        else:
            selected_activity = eligible_activities.pop(0)

        # Определяем самое раннее возможное время начала операции
        earliest_start = max(
            [schedule_start_times.get(pred, 0) + operations[pred]['duration'] for pred in operations[selected_activity]['predecessors']],
            default=0
        )
        start_time = earliest_start

        # Цикл для проверки доступности ресурсов и предотвращения конфликтов
        while True:
            resource_usage = {r: 0 for r in resources.keys()}
            conflict = False
            conflict_end_time = start_time

            for other_act, other_start in schedule_start_times.items():
                other_end = other_start + operations[other_act]['duration']

                if not (other_start >= start_time + operations[selected_activity]['duration'] or other_end <= start_time):
                    for r in operations[other_act]['resources']:
                        if r in resource_usage:  # Убедимся, что ресурс существует в словаре
                            resource_usage[r] += 1

            for r in operations[selected_activity]['resources']:
                if r in resource_usage:  # Убедимся, что ресурс существует в словаре
                    resource_usage[r] += 1

            # Проверка на конфликты по ресурсам
            for r in resources.keys():
                if resource_usage[r] > resources[r]:
                    conflict = True
                    conflict_end_time = max(conflict_end_time, other_end)
                    break

            if not conflict:
                break
            
            start_time = conflict_end_time

        # Фиксируем время начала и конца операции
        schedule_start_times[selected_activity] = start_time
        scheduled_activities.append(selected_activity)

        # Обновление временных характеристик операции
        delta = start_time - operations[selected_activity]['early_start']
        operations[selected_activity]['early_start'] += delta
        operations[selected_activity]['early_finish'] += delta
        operations[selected_activity]['late_start'] += delta
        operations[selected_activity]['late_finish'] += delta

    total_duration = max(op['early_finish'] for op in operations.values())
    return scheduled_activities, total_duration