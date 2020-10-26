#!/usr/bin/python3
# json2mqtt - simple MQTT publishing of online JSON sources
#
# Written and (C) 2020 by Lubomir Kamensky <lubomir.kamensky@gmail.com>
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
import configparser
import signal
import json
from urllib import request
import os
    
parser = argparse.ArgumentParser(description='Simple MQTT publishing of online JSON sources')
parser.add_argument('--configuration', help='Configuration file. Required!')
args=parser.parse_args()

config = configparser.ConfigParser()
config.read(os.path.join(sys.path[0], args.configuration))

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

topic=config['MQTT']['topic']
if not topic.endswith("/"):
    topic+="/"
frequency=int(config['MQTT']['frequency'])

lastValue = {}

class Element:
    def __init__(self,row):
        self.topic=row[0]
        self.value=row[1]

    def publish(self):
        try:
            if self.value!=lastValue.get(self.topic,0) or config['MQTT']['onlychanges'] == 'false':
                lastValue[self.topic] = self.value
                fulltopic=topic+self.topic
                logging.info("Publishing " + fulltopic)
                mqc.publish(fulltopic,self.value,qos=0,retain=False)

        except Exception as exc:
            logging.error("Error reading "+self.topic+": %s", exc)

try:
    mqc=mqtt.Client()
    mqc.connect(config['MQTT']['host'],int(config['MQTT']['port']),10)
    mqc.loop_start()

    print("Reading data from URL: " + config['JSON']['url'])
    
    while True:
        source = request.urlopen(config['JSON']['url'],timeout=2)
        dataSet = json.loads(source.read())

        data = []

        for key, value in config['Mapping'].items():
            row = [key]
            row.insert(1,eval(value))
            data.append(row)

        elements=[]
        
        for row in data:
            e=Element(row)
            elements.append(e)

        for e in elements:
            e.publish()
            time.sleep(0.05)
        
        time.sleep(int(frequency))

except Exception as e:
    logging.error("Unhandled error [" + str(e) + "]")
    sys.exit(1)