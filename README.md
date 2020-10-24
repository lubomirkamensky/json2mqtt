json2mqtt
=========
Simple MQTT publishing of online JSON sources.
(C) 2020 Lubomir Kamensky <lubomir.kamensky@gmail.com> 


Dependencies
------------
* Eclipse Paho for Python - http://www.eclipse.org/paho/clients/python/


Example use
-----------
python3 json2mqtt.py --configuration davis.ini

python3 json2mqtt.py --configuration neurio.ini

Example use pm2 usage
---------------------
pm2 start /usr/bin/python3 --name "json2mqtt-davis" -- /home/luba/git/json2mqtt/json2mqtt.py --configuration davis.ini

pm2 start /usr/bin/python3 --name "json2mqtt-neurio" -- /home/luba/git/json2mqtt/json2mqtt.py --configuration neurio.ini

pm2 save