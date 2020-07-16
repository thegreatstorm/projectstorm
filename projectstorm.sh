echo "============================="
echo "====== Project Storm ========"
echo "=== Created By Storm ========"
echo "==== Docker Game Servers ===="
echo "=== Centos Support only ====="

if [[ "$1" == "start" ]]; then
   echo "Starting Server"
   nohup python projectstorm.py &> var/log/services.log &

elif [[ "$1" == "stop" ]]; then
   echo "Stopping ProjectStorm..."
   pid_file="var/run/projectstorm.pid"
   if [ -f "${pid_file}" ];then
      pid=$(cat $pid_file)
      echo $pid
      if [ -f /proc/$pid/environ ];then
         kill $pid
         echo "Killed ProjectStorm!"
         rm $pid_file
         exit 0
      else
         echo "Process indicated by PID file does not exist.  ProjectStorm is already stopped"
         rm $pid_file
         exit 0
      fi
   else
      echo "There is no pid file"
   fi

elif [[ "$1" == "install-py" ]]; then
   echo "Installing Dockerfile"
   python -m pip install -r install_stuff/requirements.txt

elif [[ "$1" == "install-dockerfile" ]]; then
   echo "Installing Dockerfile"
   cd install_stuff/
   docker build -t gameserver:latest .

else
   echo "No Argument Found Please follow the instructions below"
   echo "start.sh <start|stop|install-py|install-dockerfile>"

fi