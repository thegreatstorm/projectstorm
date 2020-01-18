import logging
import os


def log_controller(script_dir, app_name, log_path):
    prefix_dir = os.path.abspath(os.path.join(script_dir))
    log_path = os.path.abspath(os.path.join(prefix_dir, log_path))

    logger = logging.getLogger(app_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(levelname)s pid %(process)d - %(module)s : %(message)s")
    log_handler = logging.FileHandler(log_path)
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

    return logger