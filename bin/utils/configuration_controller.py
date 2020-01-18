import os
import configparser


def config_controller(script_dir, default, local):

    config = configparser.RawConfigParser()
    prefix_dir = os.path.abspath(os.path.join(script_dir))
    default_config_path = os.path.abspath(os.path.join(prefix_dir, default))
    local_config_path = os.path.abspath(os.path.join(prefix_dir, local))

    config.read(default_config_path)
    if os.path.isfile(local_config_path):
        config.read(local_config_path)

    return config
