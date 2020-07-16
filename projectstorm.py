from flask import Flask, request
from flask_restful import Api,Resource
import json
import os
import uuid

from bin.utils.configuration_controller import config_controller
from bin.utils.logging_controller import log_controller
from bin.servers import create_servers
from bin.utils.database_controller import health_check, server_info, delete_container_info
from bin.utils.auth import check_rest_key

script_dir = os.path.dirname(os.path.abspath(__file__))


# ================ Configuration Piece ===================
config_settings = config_controller(script_dir, "confs/default.conf", "confs/local.conf")
app_name = config_settings.get('general', 'app_name')
version = config_settings.get('general', 'version')
app = Flask(app_name)
api = Api(app)
host = config_settings.get('system', 'host')
port = int(config_settings.get('system', 'port'))
api_key = config_settings.get('system', 'api_key')
# ================ Configuration Piece ===================

# ================ Retrieve Logging info =================
log_path = config_settings.get('logging', 'log_path')
logger = log_controller(script_dir, app_name, log_path)
# ================ Retrieve Logging info =================

# ================ Database info =================
db_path = config_settings.get('database', 'db_path')
health_check(logger, script_dir, db_path)
# ================ Database info =================


logger.info("Starting App: {} - Version: {}".format(app_name, version))
logger.debug("Configurations Address: {} - Port: {} - Api Key: {}".format(host, port, api_key))


@app.route('/projectstorm/create_servers', methods=['POST'])
def create_server():
    data = request.data
    data = json.loads(data)
    pid = uuid.uuid1()

    status = check_rest_key(data, api_key)
    if status == 401:
        logger.warning("work_thread {} - Someone tried to touch me without permission.".format(pid))
        return "Failed api_key", 401

    logger.info("work_thread {} - Starting work.".format(pid))
    response = create_servers(logger, db_path, data, pid)
    return response, 200


@app.route('/projectstorm/get_server_info', methods=['POST'])
def get_server_info():
    data = request.data
    data = json.loads(data)
    pid = uuid.uuid1()

    status = check_rest_key(data, api_key)
    if status == 401:
        logger.warning("work_thread {} - Someone tried to touch me without permission.".format(pid))
        return "Failed api_key", 401

    logger.info("work_thread {1} - Getting Server Info for {0}".format(data["container_id"], pid))
    response = server_info(logger, db_path, data["container_id"])
    return response, 200


@app.route('/projectstorm/delete_server_info', methods=['POST'])
def delete_server_info():
    data = request.data
    data = json.loads(data)
    pid = uuid.uuid1()

    status = check_rest_key(data, api_key)
    if status == 401:
        logger.warning("work_thread {} - Someone tried to touch me without permission.".format(pid))
        return "Failed api_key", 401

    logger.info("work_thread {1} - Deleting Server Info for {0}".format(data["container_id"], pid))
    response = delete_container_info(logger, db_path, data["container_id"])
    return response, 200


app.run(host=host, port=port, debug=True)
