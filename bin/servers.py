from bin.game_servers.rust import create_rust_server


def create_servers(logger, db_path, server_type):
    response = {}
    response["status"] = "I broke I think"


    if 'rust' == server_type:
        logger.info("I'm creating a rust server!")
        response["status"] = create_rust_server(logger, db_path, response)
    elif 'ark' == server_type:
        logger.info("I'm creating a ark server!")
        response["status"] = "I can't create {}. I don't know how".format(server_type)
    elif 'minecraft' == server_type:
        logger.info("I'm creating a minecraft server!")
        response = "I can't create {}. I don't know how".format(server_type)

    return response

