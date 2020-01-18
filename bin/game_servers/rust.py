from subprocess import check_output, Popen
import socket
from bin.utils.random_password import random_password
from bin.utils.random_port import random_port
from bin.utils.database_controller import insert_container_info

def create_rust_server(logger, db_path, response):
    response = {}
    game_port = random_port()
    rcon_port = random_port()
    ssh_port = random_port()

    command = "docker run -td -p {0}:{0}/udp -p {0}:{0}/tcp -p {1}:{1}/tcp -p {2}:22 gameserver".format(game_port, rcon_port, ssh_port)

    linuxgsm_password = random_password()
    root_password = random_password()

    try:
        container_id = check_output(command, shell=True)
        container_id = container_id.rstrip("\n\r")
        logger.info("I have created a container: {}".format(container_id))

        response["container_id"] = container_id
        response["game_port"] = game_port
        response["rcon_port"] = rcon_port
        response["ssh_port"] = ssh_port
        response["status"] = "Successfully created Server"
        response["user_password"] = linuxgsm_password
        response["root_password"] = root_password
        response["server_type"] = "rust"
        insert_container_info(logger, db_path, response)
    except Exception as e:
        response["status"] = "Failed to create container. {}".format(str(e))

    return response
