import paho.mqtt.client as mqtt
from pynput.keyboard import Key, Controller
import json, os
DEBUG=True
TOPIC='zigbee2mqtt/+/action'

#########################################################################
def on_connect(client, userdata, flags, rc):
    printc("[+] Connected with result code "+str(rc))
    client.subscribe(TOPIC)
    printc("[+] Subscribed to " + TOPIC)

def on_message(client, userdata, msg):
    _, device, _ = msg.topic.split('/')
    if ((device in config['devices'])):
        action = msg.payload.decode()
        if (action in config['devices'][device]):
            print_message(device, action)
            keyboard.press(Key[config['devices'][device][action]])
            keyboard.release(Key[config['devices'][device][action]])
        else:
            print_unmapped(device, action)

def print_message(device, action):
    printc("[+] "+device+": "+action+" --> "+config['devices'][device][action])

def print_unmapped(device, action):
    printc("[!] "+device+": "+action+" is unmapped!")

def printc(s):
    if(DEBUG):
        print(s)
#########################################################################

dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'
with open(dir_path + 'config.json') as f:
    config = json.load(f)

keyboard = Controller()

client = mqtt.Client()
client.username_pw_set(config['connection']['username'],config['connection']['password'])
client.on_connect = on_connect
client.on_message = on_message

client.connect(config['connection']['host'], config['connection']['port'], 60)
client.loop_forever()
