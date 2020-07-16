import os


def create_pid(logger, script_dir, pid_path):
    try:
        prefix_dir = os.path.abspath(os.path.join(script_dir))
        pid_location = os.path.abspath(os.path.join(prefix_dir, pid_path))

        # Initialize the app
        with open(pid_location, "w") as fh:
            fh.write(str(os.getpid()))
    except Exception as e:
        logger.error("Failed to create pid Check permissions or your confs for pid_location")