from subprocess import check_output, Popen
import socket
import threading

from bin.utils.random_password import random_password
from bin.utils.random_port import random_port
from bin.utils.database_controller import insert_container_info


def command_prefix(container_id, command):
    main_command = 'docker exec -t -u linuxgsm {0} sh -c "{1}"'.format(container_id, command)

    return main_command


def create_rust_server(logger, db_path, data, pid):
    game_port = random_port()
    rcon_port = random_port()
    ssh_port = random_port()

    if not data.get("max_players"):
        data["max_players"] = "250"

    if data["max_players"] == "":
        data["max_players"] = "250"

    command = "docker run -td -p {0}:{0}/udp -p {0}:{0}/tcp -p {1}:{1}/tcp -p {2}:22 gameserver".format(game_port, rcon_port, ssh_port)

    linuxgsm_password = random_password()
    root_password = random_password()

    try:
        container_id = check_output(command, shell=True)
        container_id = container_id.rstrip("\n\r")
        logger.info("work_thread {0} - I have created a container: {1}".format(pid, container_id))

        data["container_id"] = container_id
        data["game_port"] = game_port
        data["rcon_port"] = rcon_port
        data["ssh_port"] = ssh_port
        data["status"] = "Successfully created Server, please give it 5 minutes"
        data["user_password"] = linuxgsm_password
        data["root_password"] = root_password
        data["server_type"] = "rust"

        insert_container_info(logger, db_path, data)
        thread = threading.Thread(target=install_rust_server, args=(logger, data, pid))
        thread.start()

    except Exception as e:
        logger.error("work_thread {0} - Failed to create container: {1}".format(pid, str(e)))
        data["status"] = "Failed to create container. {}".format(str(e))

    return data


def install_rust_server(logger, data, pid):
    # Changes root and linuxgsm passwords so hackers can't ssh to default passwords
    change_passwords(logger, data, pid)

    try:
        # Installs rust server
        logger.info("work_thread {0} - Container: {1} - Starting Rust Installation".format(pid, data["container_id"]))
        check_output(command_prefix(data["container_id"], '/home/linuxgsm/./linuxgsm.sh rustserver'), shell=True)
        check_output(command_prefix(data["container_id"], 'yes Y | /home/linuxgsm/./rustserver install'), shell=True)

    except Exception as e:
        logger.error("work_thread {0} - Failed to install rust container. {1}. Exception: {2}".format(pid, data["container_id"], str(e)))
        data["status"] = "Failed to install rust container. {0}. Exception: {1}".format(data["container_id"], str(e))

    # Creates the rustserver.cfg required for the container
    rust_configuration(logger, data, pid)

    # Starting Rust Server
    start_rust_server(logger, data, pid)


def change_passwords(logger, data, pid):
    try:
        logger.info("work_thread {0} - Container: {1} - Starting Rust Server".format(pid, data["container_id"]))
        check_output(command_prefix(data["container_id"], 'echo \"root:{}\" | chpasswd'.format(data["root_password"])), shell=True)
        check_output(command_prefix(data["container_id"], 'echo \"linuxgsm:{}\" | chpasswd'.format(data["user_password"])), shell=True)
    except Exception as e:
        logger.error("work_thread {0} - Failed to change passwords {1}. Exception: {2}".format(pid, data["container_id"], str(e)))


def start_rust_server(logger, data, pid):
    try:
        logger.info("work_thread {0} - Container: {1} - Starting Rust Server".format(pid, data["container_id"]))
        check_output(command_prefix(data["container_id"], '/home/linuxgsm/./rustserver start'), shell=True)
    except Exception as e:
        logger.error("work_thread {0} - Failed to change passwords {1}. Exception: {2}".format(pid, data["container_id"], str(e)))


def stop_rust_server(logger, data, pid):
    try:
        logger.info("work_thread {0} - Container: {1} - Stopping Rust Server".format(pid, data["container_id"]))
        check_output(command_prefix(data["container_id"], '/home/linuxgsm/./rustserver stop'), shell=True)
    except Exception as e:
        logger.error("work_thread {0} - Failed to Stop Rust Server. {1}. Exception: {2}".format(pid, data["container_id"], str(e)))


def rust_configuration(logger, data):
    try:
        logger.info("work_thread {0} - Container: {1} - Prepping rustserver.cfg".format(pid, data["container_id"]))
        check_output(command_prefix(data["container_id"], 'echo port=\"{}\" > /home/linuxgsm/lgsm/config-lgsm/rustserver/rustserver.cfg'.format( data["game_port"])), shell=True)
        check_output(command_prefix(data["container_id"], 'echo rconport=\"{}\" >> /home/linuxgsm/lgsm/config-lgsm/rustserver/rustserver.cfg'.format(data["rcon_port"])), shell=True)
        check_output(command_prefix(data["container_id"], 'echo rconpassword=\"{}\" >> /home/linuxgsm/lgsm/config-lgsm/rustserver/rustserver.cfg'.format(data["user_password"])), shell=True)
        check_output(command_prefix(data["container_id"], 'echo rconweb=\"1\" >> /home/linuxgsm/lgsm/config-lgsm/rustserver/rustserver.cfg'), shell=True)
        check_output(command_prefix(data["container_id"], 'echo servername=\"{}\" >> /home/linuxgsm/lgsm/config-lgsm/rustserver/rustserver.cfg'.format(data["server_name"])), shell=True)
        check_output(command_prefix(data["container_id"], 'echo maxplayers=\"{}\" >> /home/linuxgsm/lgsm/config-lgsm/rustserver/rustserver.cfg'.format(data["maxplayers"])), shell=True)
        check_output(command_prefix(data["container_id"], 'echo seed=\"{}\" >> /home/linuxgsm/lgsm/config-lgsm/rustserver/rustserver.cfg'.format(data["seed"])), shell=True)
        check_output(command_prefix(data["container_id"], 'echo worldsize=\"{}\" >> /home/linuxgsm/lgsm/config-lgsm/rustserver/rustserver.cfg'.format(data["worldsize"])), shell=True)

    except Exception as e:
        logger.error("Failed to install rust container. {0}. Exception: {1}".format(data["container_id"], str(e)))
