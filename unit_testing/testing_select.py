import sqlite3


def select(db_path):
    conn = sqlite3.connect(db_path)
    command = "SELECT * FROM SERVERS"
    cursor = conn.execute(command)
    desc = cursor.description
    response = {}

    for row in cursor:
        i = 0
        while i < len(row):
            response[desc[i][0]] = row[i]
            i += 1

    return response


response = select("../db/storm.db")
print(response)