from bin.game_servers.rust import create_rust_server


def create_servers(logger, db_path, data, pid):
    response = {}
    response["status"] = "I broke I think"

    if 'rust' == data["server_type"]:
        logger.info("work_thread {} - I'm creating a rust server!".format(pid))
        response = create_rust_server(logger, db_path, data, pid)
    elif 'ark' == data["server_type"]:
        logger.info("work_thread {} - I'm creating a ark server!".format(pid))
        response["status"] = "I can't create {}. I don't know how".format(data["server_type"])
    elif 'minecraft' == data["server_type"]:
        logger.info("work_thread {} - I'm creating a minecraft server!".format(pid))
        response["status"] = "I can't create {}. I don't know how".format(data["server_type"])

    return response

