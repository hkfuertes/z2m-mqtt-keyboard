import paho.mqtt.client as mqtt
from pynput.keyboard import Key, Controller
import json, os

#########################################################################
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(config['topic'])
    print("Subscribed to " + config['topic'])

def on_message(client, userdata, msg):
    key_pressed = json.loads(msg.payload)['action']
    if (key_pressed != ""):
        print(key_pressed + " --> " + config['keys'][key_pressed])
        keyboard.press(Key[config['keys'][key_pressed]])
        keyboard.release(Key[config['keys'][key_pressed]])
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
