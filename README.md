json2mqtt
=========
Simple MQTT publishing of online JSON sources.
(C) 2018 Lubomir Kamensky <lubomir.kamensky@gmail.com> 


Dependencies
------------
* Eclipse Paho for Python - http://www.eclipse.org/paho/clients/python/


Command line options
--------------------
    usage: jason2mqtt.py [-h] [--mqtt-host MQTT_HOST]  [--mqtt-port MQTT_PORT]
                         [--mqtt-topic MQTT_TOPIC] --json JSON
                         --map MAP [--frequency FREQUENCY ]
    
    optional arguments:
      -h, --help            show this help message and exit
      --mqtt-host MQTT_HOST
                            MQTT server address. Defaults to "localhost"
      --mqtt-port MQTT_PORT
                            MQTT server port. Defaults to 1883
      --mqtt-topic MQTT_TOPIC
                            Topic prefix to be used for subscribing/publishing.
                            Defaults to "json"
      --frequency FREQUENCY
                            How often is the JSON source checked for the changes,
                            in seconds. Only integers. Defaults to 1 


JSON
----
URL of online JSON source to be published via MQTT.

Example:  Local access to Neur.io sensor 

http://192.168.88.189/current-sample 

Example data:

{"sensorId":"0x0000C47F510180C9","timestamp":"2018-02-01T17:12:30Z","channels":[{"type":"PHASE_A_CONSUMPTION","ch":1,"eImp_Ws":4853108845,"eExp_Ws":1792905,"p_W":116,"q_VAR":-72,"v_V":239.253},{"type":"PHASE_B_CONSUMPTION","ch":2,"eImp_Ws":4641133741,"eExp_Ws":3195780,"p_W":80,"q_VAR":-85,"v_V":232.178},{"type":"PHASE_C_CONSUMPTION","ch":3,"eImp_Ws":6804918537,"eExp_Ws":15110144,"p_W":143,"q_VAR":-110,"v_V":236.615},{"type":"CONSUMPTION","ch":4,"eImp_Ws":16293113391,"eExp_Ws":14269510,"p_W":338,"q_VAR":-267,"v_V":236.015}],"cts":[{"ct":1,"p_W":116,"q_VAR":-72,"v_V":239.253},{"ct":2,"p_W":80,"q_VAR":-85,"v_V":232.178},{"ct":3,"p_W":143,"q_VAR":-110,"v_V":236.615},{"ct":4,"p_W":0,"q_VAR":0,"v_V":239.210}]}


MAP
---
JSON transformation mapping using list or set comprehension.

Example: See file neurio.txt where the original JSON data is refferred to as "dataSet"

[ (i['type'],i['p_W']) for i in dataSet['channels'] ]

Result using Example data and mapping file: 

[('PHASE_A_CONSUMPTION', 116), ('PHASE_B_CONSUMPTION', 80), ('PHASE_C_CONSUMPTION', 143), ('CONSUMPTION', 338)]


Example usage:
--------------

python3 json2mqtt.py --json http://192.168.88.189/current-sample --map neurio.txt --mqtt-topic neurio

And resulting MQTT publishing:

neurio/PHASE_A_CONSUMPTION 116

neurio/PHASE_B_CONSUMPTION 80

neurio/PHASE_C_CONSUMPTION 143

neurio/CONSUMPTION 338



production usage with PM2:
--------------------------
PM2: https://www.npmjs.com/package/pm2

pm2 start /usr/bin/python3 --name "json2mqtt-neurio" -- /home/luba/Git/json2mqtt/json2mqtt.py --json http://192.168.88.189/current-sample --map neurio.txt --mqtt-topic neurio

pm2 save

