import json
import requests
import time
import paho.mqtt.client as paho
import os

PUBLISH_DISCOVERY = os.environ.get('DISCOVERY') != None or False
LOGGING = os.environ.get('LOGGING') != None or False
removeDiscovery = False

client= paho.Client("client-001")

u = os.environ.get('USER')
p = os.environ.get('PASS')
if u != None and p != None:
    client.username_pw_set(username=u, password=p)


client.connect(os.environ.get('BROKER'))


# urlfile = "http://gagnaveita.vegagerdin.is/api/faerd2017_1"
url = "http://gagnaveita.vegagerdin.is/api/vedur2014_1"

response = requests.get(url).json()

for vedur in response:

    itemId = vedur['Nr']
    name = vedur['Nafn']

    ## config topics
    temp_config_topic = "homeassistant/sensor/vedur{}temp/config".format(itemId)
    humidity_config_topic = "homeassistant/sensor/vedur{}humidity/config".format(itemId)
    wind_config_topic = "homeassistant/sensor/vedur{}wind/config".format(itemId)
    windburst_config_topic = "homeassistant/sensor/vedur{}windburst/config".format(itemId)
    pressure_config_topic = "homeassistant/sensor/vedur{}pressure/config".format(itemId)
    traffic_config_topic = "homeassistant/sensor/vedur{}traffic/config".format(itemId)

    state_topic =  "homeassistant/sensor/vedur{}/state".format(itemId)
    
    ## temperature topic
    temperaturePayloadConfigJson = {
        "name": "{} hiti".format(name), 
        "device_class": "temperature", 
        "unit_of_measurement": "°C", 
        "state_topic": state_topic, 
        "value_template": "{{ value_json.Hiti }}" 
    }
    temperaturePayloadConfig = json.dumps(temperaturePayloadConfigJson)

    ## humidity topic
    humidityPayloadConfigJson = {
        "name": "{} raki".format(name), 
        "device_class": "humidity",
        "unit_of_measurement": "%", 
        "state_topic": state_topic, 
        "value_template": "{{ value_json.Raki }}" 
    }
    humidityPayloadConfig = json.dumps(humidityPayloadConfigJson)

    ## wind topic
    windPayloadConfigJson = {
        "name": "{} vindur".format(name), 
        "unit_of_measurement": "m/s", 
        "state_topic": state_topic, 
        "value_template": "{{ value_json.Vindhradi }}" 
    }
    windPayloadConfig = json.dumps(windPayloadConfigJson)

    ## wind topic
    windburstPayloadConfigJson = {
        "name": "{} vindhviður".format(name), 
        "unit_of_measurement": "m/s", 
        "state_topic": state_topic, 
        "value_template": "{{ value_json.Vindhvida }}" 
    }
    windburstPayloadConfig = json.dumps(windburstPayloadConfigJson)

    ## pressure topic    
    pressurePayloadConfigJson = {
        "name": "{} loftþrýstingur".format(name), 
        "unit_of_measurement": "hPa", 
        "state_topic": state_topic, 
        "value_template": "{{ value_json.Loftthrystingur }}" 
    }
    pressurePayloadConfig = json.dumps(pressurePayloadConfigJson)

    ## pressure topic
    trafficPayloadConfigJson = {
        "name": "{} umferð".format(name), 
        "unit_of_measurement": "Bílar", 
        "state_topic": state_topic,
        "value_template": "{{ value_json.UmfSum }}" 
    }
    trafficPayloadConfig = json.dumps(trafficPayloadConfigJson)

    if removeDiscovery:
        client.publish(temp_config_topic, "")
        client.publish(humidity_config_topic, "")
        client.publish(wind_config_topic, "")
        client.publish(windburst_config_topic, "")
        client.publish(pressure_config_topic, "")
        client.publish(traffic_config_topic, "")
        
        continue

    if PUBLISH_DISCOVERY:
        print("Publishing discovery..")
        client.publish(temp_config_topic, temperaturePayloadConfig)
        client.publish(humidity_config_topic, humidityPayloadConfig)
        client.publish(wind_config_topic, windPayloadConfig)
        client.publish(windburst_config_topic, windburstPayloadConfig)
        client.publish(pressure_config_topic, pressurePayloadConfig)
        client.publish(traffic_config_topic, trafficPayloadConfig)

    # Actual data
    payloadData = json.dumps(vedur, separators=(',', ':'))
    client.publish(state_topic, payloadData)
    
    if LOGGING:
        print("{}: {}".format(state_topic, payloadData))

