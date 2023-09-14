# zigbee2mqtt keyboard
Simple script that connects to the mqtt topic of z2m and listens for actions and converts them to key strokes.

## Example config file
You can look for the special characters list [here](https://github.com/moses-palmer/pynput/blob/master/lib/pynput/keyboard/_base.py). The `devices` keys (the names) have to mach the names in zigbee2mqtt. If an action is not mapped, the terminal will reply the name of the action so that it can be mapped.

```json
{
    "connection": {
        "host": "",
        "port": 1883,
        "username": "",
        "password": ""
    },
    "devices": {
        "IKEA_RODRET": {
            "on": "media_volume_up",
            "off": "media_volume_down",
            "brightness_move_up": "media_volume_mute",
            "brightness_move_down": "media_play_pause"
        },
        "IKEA_5BUTTONS": {
            "toggle": ["cmd", "shift", "m"],
            "brightness_down_click": "media_volume_down",
            "brightness_up_click": "media_volume_up"
        }
    }

}
```

## Usage
To run outside a virtual environment, skip the first 2 commands:
```sh
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```