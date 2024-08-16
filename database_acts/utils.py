import pandas as pd

def export_table_to_csv(conn, table_name, output_file):
    query = f"SELECT * FROM {table_name}"
    
    df = pd.read_sql(query, conn)

    df.to_csv(output_file, index=False)

    print(f"Данные из таблицы {table_name} сохранены в {output_file}")