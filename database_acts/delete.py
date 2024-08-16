
def drop_table(cur, table):
    cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
    print(f"Таблица {table} удалена.")


def drop_all_tables(cur):
    cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' """)

    tables = cur.fetchall()

    for table in tables:
        cur.execute(f"DROP TABLE IF EXISTS {table[0]} CASCADE")
        print(f"Таблица {table[0]} удалена.")