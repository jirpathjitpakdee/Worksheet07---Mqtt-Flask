from flask import Flask, jsonify, render_template
import requests
from paho.mqtt import client as mqtt_client
from flask_cors import CORS
import time

broker = "172.20.10.3"
port = 1883


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client("server")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


app = Flask(__name__)
CORS(app)
server_ip = "http://172.20.10.3:4000"
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/thingspeak")
def thingspeak():
    headers = {'Accept': 'application/json'}
    #https://thingspeak.com/channels/12397/feed.json
    url = "https://thingspeak.com/channels/161401/field/5.json"
    r = requests.get(url, headers=headers)
    return r.json();

@app.route("/nodemcu/last")
def nodemcu():
    headers = {'Accept': 'application/json'}
    r = requests.get(server_ip+'/sensors?_sort=id&_order=desc&_limit=1', headers=headers)
    return r.json();

@app.route("/nodemcu/data")
def nodemcuData():
    headers = {'Accept': 'application/json'}
    r = requests.get(server_ip+'/sensors', headers=headers)
    return r.json();

@app.route("/nodemcu/led/on")
def led_publishOn():
    client = connect_mqtt()
    client.loop_start()
    result =  client.publish("led", "on")
    time.sleep(2)
    client.loop_stop()
    r = {'status':"OK"}
    return  r

@app.route("/nodemcu/led/off")
def led_publishOff():
    client = connect_mqtt()
    client.loop_start()
    result = client.publish("led", "off")
    time.sleep(2)
    client.loop_stop()
    r = {'status':"OK"}
    return  r

if __name__ == "__main__":
   
    app.run(host='0.0.0.0', debug=True)