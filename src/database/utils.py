import pandas as pd

def export_table_to_csv(conn, table_name, output_file) -> None:
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    df.to_csv(output_file, index=False)

    print(f"Данные из таблицы {table_name} сохранены в {output_file}")