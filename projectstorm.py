from flask import Flask, request
from flask_restful import Api,Resource
import json
import os
import uuid

from bin.utils.configuration_controller import config_controller
from bin.utils.logging_controller import log_controller
from bin.servers import create_servers
from bin.utils.database_controller import health_check, server_info

script_dir = os.path.dirname(os.path.abspath(__file__))


# ================ Configuration Piece ===================
config_settings = config_controller(script_dir, "confs/default.conf", "confs/local.conf")
app_name = config_settings.get('general', 'app_name')
app = Flask(app_name)
api = Api(app)
host = config_settings.get('general', 'host')
port = int(config_settings.get('general', 'port'))
# ================ Configuration Piece ===================

# ================ Retrieve Logging info =================
log_path = config_settings.get('general', 'log_path')
logger = log_controller(script_dir, app_name, log_path)
logger.info("I have started")
# ================ Retrieve Logging info =================

# ================ Database info =================
db_path = config_settings.get('database', 'db_path')
health_check(logger, script_dir, db_path)
# ================ Database info =================


@app.route('/projectstorm/create_servers', methods=['POST'])
def create_server():
    data = request.data
    data = json.loads(data)
    pid = uuid.uuid1()
    logger.info("work_thread {} - Starting work.".format(pid))
    response = create_servers(logger, db_path, data, pid)
    return response, 200


@app.route('/projectstorm/get_server_info', methods=['POST'])
def get_server_info():
    data = request.data
    data = json.loads(data)
    pid = uuid.uuid1()
    logger.info("work_thread {1} - Getting Server Info for {0}".format(data["container_id"], pid))
    response = server_info(logger, db_path, data["container_id"])
    return response, 200


app.run(host=host, port=port, debug=True)