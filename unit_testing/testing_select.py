import sqlite3

def select(db_path, container_id):
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

response = select("storm.db", "f3953e1c69aeb935011c4062928d637537f41dc773356c359aa8ea9511a1d20a")
print(response)