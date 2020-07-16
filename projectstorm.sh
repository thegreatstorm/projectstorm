echo "============================="
echo "====== Project Storm ========"
echo "=== Created By Storm ========"
echo "==== Docker Game Servers ===="
echo "=== Centos Support only ====="

if [[ "$1" == "start" ]]; then
   echo "Starting Server"
   nohup python projectstorm.py &

elif [[ "$1" == "stop" ]]; then
   echo "Stopping Server"
   ps aux | grep -ie projectstorm.py | awk '{print $2}' | xargs kill -9

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