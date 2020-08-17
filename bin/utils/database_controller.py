import os
import sqlite3


def health_check(logger, script_dir, db_path):
    logger.info("Health Check for Database")
    prefix_dir = os.path.abspath(os.path.join(script_dir))
    db_path = os.path.abspath(os.path.join(prefix_dir, db_path))

    logger.debug("Database location {}".format(db_path))
    if not os.path.isfile(db_path):
        logger.warning("Database not found under path {}".format(db_path))
        f = open(db_path, "w+")
        f.close()
        logger.debug("Created new Database")
        create_table(logger, db_path)
    else:
        logger.debug("Database exists!~")


def create_table(logger, db_path):
    conn = sqlite3.connect(db_path)
    logger.debug("Creating Tables")
    try:
        conn.execute('''CREATE TABLE servers
                 (container_id TEXT PRIMARY KEY     NOT NULL,
                 game_port            INT     NOT NULL,
                 mobile_port            INT     NOT NULL,
                 rcon_port            INT     NOT NULL,
                 ssh_port            INT     NOT NULL,
                 status           TEXT    NOT NULL,
                 server_type           TEXT    NOT NULL,
                 root_password           TEXT    NOT NULL,
                 user_password           TEXT    NOT NULL);''')
        logger.debug("Created Tables Successfully")
    except Exception as e:
        logger.error("Couldn't create table! {}".format(str(e)))
    conn.close()


def insert_container_info(logger, db_path, response):
    try:
        conn = sqlite3.connect(db_path)
        command = "INSERT INTO servers (container_id, game_port, mobile_port, rcon_port, ssh_port, status, server_type, root_password, user_password) \
        VALUES('{0}', {1}, {2}, {3}, {4}, '{5}', '{6}', '{7}', '{8}')".format(
            response["container_id"],
            response["game_port"],
            response["mobile_port"],
            response["rcon_port"],
            response["ssh_port"],
            response["status"],
            response["server_type"],
            response["root_password"],
            response['user_password'])
        conn.execute(command)
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error("Inserting container to database failed! {}".format(str(e)))


def delete_container_info(logger, db_path, container_id):
    logger.debug("Deleting container")

    response = {}
    response["container_id"] = container_id
    try:
        conn = sqlite3.connect(db_path)
        command = "DELETE FROM servers WHERE container_id = '{}'".format(container_id)
        conn.execute(command)
        conn.commit()
        conn.close()
        response["status"] = "Deleted"
    except Exception as e:
        response["status"] = "Failed To Delete"
        logger.error("Delete container to database failed! {}".format(str(e)))

    return response


def update_server_info(logger, db_path, sql):
    try:
        conn = sqlite3.connect(db_path)
        conn.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error("Update container to database failed! {}".format(str(e)))


def server_info(logger, db_path, container_id):
    conn = sqlite3.connect(db_path)
    command = "SELECT * FROM servers WHERE container_id = '{}'".format(container_id)
    cursor = conn.execute(command)
    desc = cursor.description
    response = {}

    for row in cursor:
        i = 0
        while i < len(row):
            response[desc[i][0]] = row[i]
            i += 1

    return response
