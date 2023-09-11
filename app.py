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
            to_stroke = config['devices'][device][action]
            if(isArray(to_stroke)):
                print_message(device, action, to_stroke)
                with keyboard.pressed(*list(map(lambda k: Key[k], to_stroke[:-1]))):
                    press_key(to_stroke[-1])
            else:
                print_message(device, action, to_stroke)
                press_key(to_stroke)
        else:
            print_unmapped(device, action)

def press_key(key_name):
    if(key_name in Key.__members__):
        key = Key[key_name]
    else:
        key = key_name
    keyboard.press(key)
    keyboard.release(key)

def isArray(var):
    return isinstance(var, (list, tuple))

def print_message(device, action, to_stroke):
    printc("[+] "+device+": "+action+" --> " + str(to_stroke))

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
