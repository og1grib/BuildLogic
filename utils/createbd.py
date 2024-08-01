

def create_database(cur):

    cur.execute("""CREATE TABLE IF NOT EXISTS operations (
        op_id VARCHAR(255) PRIMARY KEY,
        duration INT,
        priority INT,
        release_time INT,
        predecessors TEXT,
        successors TEXT,
        resources TEXT,
        deadline INT
    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS resources (
        type VARCHAR(255) PRIMARY KEY,
        resource JSONB
    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS additional_info (
        info_id VARCHAR(255) PRIMARY KEY,
        description TEXT
    );""")
