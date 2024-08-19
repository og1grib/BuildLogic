def create_tables(cur) -> None:

    cur.execute("""CREATE TABLE IF NOT EXISTS operations (
        op_id VARCHAR(255) PRIMARY KEY,
        duration INT,
        priority INT,
        release_time INT,
        predecessors TEXT,
        successors TEXT,
        resources TEXT,
        deadline INT);""")

    cur.execute("""CREATE TABLE IF NOT EXISTS resources (
        type VARCHAR(255) PRIMARY KEY,
        quantity INT);""")

    cur.execute("""CREATE TABLE IF NOT EXISTS additional_info (
        info_id VARCHAR(255) PRIMARY KEY,
        description TEXT);""")

    cur.execute(f"""CREATE TABLE IF NOT EXISTS results (
            op_id VARCHAR(255) PRIMARY KEY,
            duration INT,
            predecessors TEXT,
            successors TEXT,
            resources TEXT,
            early_start INT,
            early_finish INT,
            late_start INT,
            late_finish INT,
            is_critical BOOLEAN);""")
    
    print(f"Таблицы operations, resources, additional_info, results успешно созданы.")
    
    