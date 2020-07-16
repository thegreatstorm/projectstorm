import requests
import json


def postRequest():
    print("You are attempting to post information for servers")

    host = ""
    port = ""
    api_key = ""

    baseurl = "http://{}:{}/projectstorm/create_servers".format(host, port)
    header = {"Content-Type": "application/json"}

    data = {}
    data["api_key"] = api_key
    data["server_type"] = "rust"
    data["seed"] = "22"
    data["worldsize"] = "1000"
    data["maxplayers"] = "250"
    data["server_name"] = ""
    json_outgoing = json.dumps(data)

    try:
        response = requests.post(baseurl, headers=header, data=json_outgoing, verify=False)
        print(response)
        print(response.text)

    except Exception as e:
        print("FAILED: " + str(e))


postRequest()