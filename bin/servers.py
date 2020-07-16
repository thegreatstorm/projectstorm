from bin.game_servers.rust import create_rust_server


def create_servers(logger, db_path, data, pid):
    response = {}
    response["status"] = "I broke I think"

    if 'rust' == data["server_type"]:
        logger.info("work_thread {} - Creating Rust Server".format(pid))
        response = create_rust_server(logger, db_path, data, pid)
    else:
        response["status"] = "No server type found."

    return response

