# ProjectStorm - Configurations
Author: TheGreatStorm

Location where you can setup configured values so if you want to run rest api more than once in different directories or systems.

local.conf overrides default.conf changes. Any value you add to local.conf will override the value in default.conf


* default.conf
  *     [general]
        app_name -> Name of the app will run. This is needed for flask.
        version -> Version gets logged on startup.      
        
        [system]
        host -> Ip address or Hostname your using for the system this will be on.
        port -> Port you want to use the flask app on.
        api_key -> Authenication key needed to interact with the app. 
        I recommend you use unit_testing/api_key_creation.py to generate a api_key  
        
        [database]
        db_path -> Location of where you want the db files to be at.
        
        [logging]
        log_path -> Location of where you want the log files to be at.
        
* local.conf - Override


