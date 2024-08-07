
def drop_table(cur):
    cur.execute(f"DROP TABLE IF EXISTS operations CASCADE;")
    cur.execute(f"DROP TABLE IF EXISTS resources CASCADE;")
    cur.execute(f"DROP TABLE IF EXISTS additional_info CASCADE;")
