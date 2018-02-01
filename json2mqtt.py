#
# json2mqtt - simple MQTT publishing of online JSON sources
#
# Written and (C) 2018 by Lubomir Kamensky <lubomir.kamensky@gmail.com>
# Provided under the terms of the MIT license
#
# Requires:
# - Eclipse Paho for Python - http://www.eclipse.org/paho/clients/python/
#

import argparse
import logging
import logging.handlers
import time
import paho.mqtt.client as mqtt
import sys
import signal
import json
from urllib import request
    
parser = argparse.ArgumentParser(description='Bridge between JSON file and MQTT')
parser.add_argument('--mqtt-host', default='localhost', help='MQTT server address. Defaults to "localhost"')
parser.add_argument('--mqtt-port', default='1883', type=int, help='MQTT server port. Defaults to 1883')
parser.add_argument('--mqtt-topic', default='json', help='Topic prefix to be used for subscribing/publishing. Defaults to "modbus/"')
parser.add_argument('--json', help='URL of JSON source')
parser.add_argument('--map', help='JSON transformation mapping using list or set comprehension')
parser.add_argument('--frequency', default='1', help='How often is the json source checked for the changes, in seconds. Only integers. Defaults to 1')

args=parser.parse_args()

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

topic=args.mqtt_topic
if not topic.endswith("/"):
    topic+="/"
frequency=int(args.frequency)

def signal_handler(signal, frame):
        print('Exiting ' + sys.argv[0])
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class Element:
    def __init__(self,row):
        self.topic=row[0]
        self.value=row[1]
        self.lastval=None

    def publish(self):
        try:
            if self.value!=self.lastval:
                self.lastval=self.value
                fulltopic=topic+self.topic
                logging.info("Publishing " + fulltopic)
                mqc.publish(fulltopic,self.lastval,qos=0,retain=True)

        except Exception as exc:
            logging.error("Error reading "+self.topic+": %s", exc)

try:
    mqc=mqtt.Client()
    mqc.connect(args.mqtt_host,args.mqtt_port,10)
    mqc.loop_start()

    while True:
        source = request.urlopen(args.json)
        dataSet = json.loads(source.read())
        data = eval(open(args.map).read())
        elements=[]

        for row in data:
            e=Element(row)
            elements.append(e)

            for e in elements:
                e.publish()
        
        time.sleep(int(frequency))

except Exception as e:
    logging.error("Unhandled error [" + str(e) + "]")
    sys.exit(1)
    