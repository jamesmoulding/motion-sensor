import serial
import paho.mqtt.client as mqtt
import time

mqttc = mqtt.Client(client_id="1596")
mqttc.username_pw_set("jamesmoulding", password="GIz2LXKM")
mqttc.connect("opensensors.io")

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)  # open first serial port
while True:
	message = ser.readline()
	print message
	mqttc.publish("/users/jamesmoulding/testing", payload=message, qos=0, retain=False)
mqttc.disconnect();
time.sleep(1);