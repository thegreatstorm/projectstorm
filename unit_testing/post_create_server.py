import requests
import json


def postRequest():
    print("You are attempting to post information for servers")

    host = input("Enter Host: ")
    port = input("Enter Port: ")
    api_key = input("Enter ApiKey: ")
    baseurl = "http://{}:{}/projectstorm/create_servers".format(host, port)
    header = {"Content-Type": "application/json"}

    outgoingJson = {}
    outgoingJson["restapi"] = api_key
    outgoingJson["server_type"] = "rust"
    json_outgoing = json.dumps(outgoingJson)


    #print(json_outgoing)

    #print("Baseurl: " + baseurl)
    try:
        response = requests.post(baseurl, headers=header, data=json_outgoing, verify=False)
        print(response)
        print(response.text)

    except Exception as e:
        print("FAILED: " + str(e))


postRequest()