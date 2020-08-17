import requests
import json


def post_server_info():
    print("You are attempting to post information for servers")

    host = input("Hostname: ")
    port = input("Port Number: ")
    api_key = input("API Key: ")
    container_id = input("Container ID: ")

    baseurl = "http://{}:{}/projectstorm/get_server_info".format(host, port)
    header = {"Content-Type": "application/json"}

    outgoingJson = {}
    outgoingJson["api_key"] = api_key
    outgoingJson["container_id"] = container_id
    json_outgoing = json.dumps(outgoingJson)

    try:
        response = requests.post(baseurl, headers=header, data=json_outgoing, verify=False)
        print(response)
        print(response.text)

    except Exception as e:
        print("FAILED: " + str(e))


post_server_info()