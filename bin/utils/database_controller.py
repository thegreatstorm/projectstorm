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
    logger.info("Creating Tables")
    try:
        conn.execute('''CREATE TABLE SERVERS
                 (CONTAINER_ID TEXT PRIMARY KEY     NOT NULL,
                 GAME_PORT            INT     NOT NULL,
                 RCON_PORT            INT     NOT NULL,
                 SSH_PORT            INT     NOT NULL,
                 STATUS           TEXT    NOT NULL,
                 SERVER_TYPE           TEXT    NOT NULL,
                 ROOT_PASSWORD           TEXT    NOT NULL,
                 USER_PASSWORD           TEXT    NOT NULL);''')
        logger.info("Created Tables Successfully")
    except Exception as e:
        logger.error("Couldn't create table! {}".format(str(e)))
    conn.close()


def insert_container_info(logger, db_path, response):
    try:
        conn = sqlite3.connect(db_path)
        command = "INSERT INTO SERVERS (CONTAINER_ID, GAME_PORT, RCON_PORT, SSH_PORT, STATUS, ROOT_PASSWORD, USER_PASSWORD, SERVER_TYPE) \
        VALUES('{}', {}, {}, {}, '{}', '{}', '{}', '{}')".format(response["container_id"], response["game_port"], response["rcon_port"], response["ssh_port"], response["status"], response["root_password"], response["user_password"],response['server_type'])
        logger.debug("SQL COMMAND: {}".format(command))
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
        command = "DELETE FROM SERVERS WHERE CONTAINER_ID = '{}'".format(container_id)
        logger.debug("SQL COMMAND: {}".format(command))
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
    command = "SELECT * FROM SERVERS WHERE CONTAINER_ID = '{}'".format(container_id)
    cursor = conn.execute(command)
    desc = cursor.description
    response = {}

    for row in cursor:
        i = 0
        while i < len(row):
            response[desc[i][0]] = row[i]
            i += 1

    return response
