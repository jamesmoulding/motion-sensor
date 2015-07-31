# motion-sensor

This simple project demonstrates pushing sensor data to OpenSensors easily using Python script.

You will need:

1 x PIR Motion Sensor
3 x jump wires
1 x Arduino Uno & USB communication cable
1 x computer or Raspberry Pi running Linux


You will need to install Mosquitto Python module, Paho MQTT client, simply type the following into CLI (Command Line):

pip install paho-mqtt

However, if you don't already have Python installed you will need to run the following command:

sudo apt-get install python-pip

You will also need a user account on OpenSensors.io, which is the IoT messaging platform we'll be using.

Lastly, you will need to install the Arduino IDE:

sudo apt-get update && sudo apt-get install arduino arduino-core  


Set up the Motion Sensor

The Motion Sensor will have three pins, some PIR sensors omit the labelling besides these pins, in that case, the pins correspond to Pin2, GND, 5V.

On the image below, the left pin & wire correspond to Pin2 on the Arduino, the central pin & wire to Ground (GND) and the right to 5V on the Arduino board.

Run the Arduino IDE, check under Tools that the serial monitor isn't greyed out. If it is greyed out, simply run Arduino IDE from CLI as superuser:


sudo arduino


You now need to load up the Arduino code for this project, https://github.com/jamesmoulding/motion-sensor/blob/master/PIR2.ino

Copy and paste this code into your Arduino IDE. Feel free to change the messages sent out by the sensor to something more suited to you... "crikey, movement detected!"

Plug your Arduino in to your Raspberry Pi or PC.

Press the Upload button and let it do it's thing. Your Arduino's LEDs should flash. Go to Tools > Serial Monitor. You should see data coming in from the sensor.

Push the data to OpenSensors

We're going to write a Python script to send the incoming serial message to the OpenSensors message broker. https://github.com/jamesmoulding/motion-sensor/blob/master/open.py

Open up a plain text editor, save the file under a name of your choice using the filetype suffix .py, for example, open.py 

In the new file we will write the following, replace examples with your own details:

The mosquitto library we need to communicate with the Opensensors message broker:


import paho.mqtt.client as mqtt


Initialise the client option with our client ID of our device. You will need to create a Device and Topic on OpenSensors before continuing:


mqttc = mqtt.Client(client_id="939") <-- replace 939 with your OpenSensors Device ID


Set our username and Device password:


mqttc.username_pw_set("John", password="AbcDEFgH")  <-- replace with username and Device password


Connect to the Opensensors server:


mqttc.connect("opensensors.io")


Let's test the device. Publish a message to say hello:


mqttc.publish("/users/John/JohnsTopic", payload="Hello Opensensors!", qos=0, retain=False) <-- replace the Topic path with your Topic path


Disconnect:


mqttc.disconnect();


Let's see if it works. Save your Python file. Open up your Topic page on OpenSensors. You should see a message "listening for messages". Enter the following command into Terminal, replace the filename with your file:


sudo python open.py 


You should see the message "Hello OpenSensors!" in your Topic message panel! 

Now let's edit this file to read the Arduino serial and send that to OpenSensors.

First, let's find out which port your arduino serial is sending to, enter into Terminal:


dmesg | grep tty


You will receive something like this:


[    0.000000] console [tty0] enabled
[ 3522.192687] cdc_acm 7-1:1.0: ttyACM0: USB ACM device


The second line has details of our Ardiuno. The ttyACM0 is the device name and ‘/dev/ttyACM0’ is the serial port.

To open and read the serial port Python makes it really easy. You can run a little test to check whether it is working by using the following code:

For communication with the Arduino we need to use the serial library:


import serial
ser = serial.Serial(‘/dev/ttyACM0’) # open first serial port
while True:
print ser.readline()        # prints each line it reads from serial


Now we bring the code we used before, and this code together:


import serial
import paho.mqtt.client as mqtt
import time

mqttc = mqtt.Client(client_id="1599")
mqttc.username_pw_set("John", password="GIz2LXKM")
mqttc.connect("opensensors.io")

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)  # open first serial port
while True:
	message = ser.readline()
	print message
	mqttc.publish("/users/John/JohnsTopic", payload=message, qos=0, retain=False)
mqttc.disconnect();
time.sleep(1);


Remember to replace with your details. Run this as before:

sudo python your_file_name_here.py 