def command_prefix(container_id, command, user):
    main_command = 'docker exec -u {0} -t {1} sh -c \'{2}\''.format(user, container_id, command)

    return main_command

data ={}
data["container_id"] = ""
data["root_password"] = ""
data["game_port"] = ""


command = command_prefix(data["container_id"], 'echo port=\\"{}\\" > /home/linuxgsm/lgsm/config-lgsm/rustserver/rustserver.cfg'.format( data["game_port"]), 'linuxgsm')

print(command)