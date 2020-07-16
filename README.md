# ProjectStorm
#### Author: TheGreatStorm

https://github.com/thegreatstorm/projectstorm.git

Why did I call it ProjectStorm? Cause Project sounds cool, and so does storm. 
Since this works with containers you can put it in a cloud and create a storm! :D

## Rest Api's
* projectstorm/create_servers
  * POST
  * Creates a container based off the json provided.
  * Required Data:
  *     data["api_key"]
        data["server_type"]
        data["seed"]
        data["worldsize"]
        data["maxplayers"]
        data["server_name"]

* projectstorm/get_server_info
  * POST
  * Retrieves information of a container requested.
  * Required Data:
  *     outgoingJson["api_key"] = api_key
        outgoingJson["container_id"] = container_id
* projectstorm/delete_server_info
  * POST
  * Deletes information of a container requested. (This does not delete the container)
  * Required Data:
  *     outgoingJson["api_key"] = api_key
        outgoingJson["container_id"] = container_id
        
## IF YOU CHANGE projectstorm.sh
I'm not very good in bash scripting.

If you update the pid_location in confs/ you will need to manually update the projectstorm.sh.