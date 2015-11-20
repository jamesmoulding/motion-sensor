import serial
import paho.mqtt.client as mqtt
import time

mqttc = mqtt.Client(client_id="1596")
mqttc.username_pw_set("YOUR_OPENSENSORS_USERNAME", password="YOUR_DEVICE_PASSWORD")
mqttc.connect("mqtt.opensensors.io")

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)  # open first serial port
while True:
	message = ser.readline()
	print message
	mqttc.publish("/users/YOUR_OPENSENSORS_USERNAME/YOUR_TOPIC_NAME", payload=message, qos=0, retain=False)
mqttc.disconnect();
time.sleep(1);
