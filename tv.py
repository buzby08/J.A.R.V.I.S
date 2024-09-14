from typing import Callable, Union
import json

from pywebostv.connection import WebOSClient
from pywebostv.controls import (
    ApplicationControl,
    InputControl,
    MediaControl,
    SourceControl,
    SystemControl,
    TvControl,
)

import speech


def connect() -> WebOSClient:
    """
    This function attempts to connect to your tv. If successful, it 
    will give you the client to allow you to control it. However, if
    unsuccessful, you will be given None.
    
    Returns:
        WebOSClient - This is returned if the connection is successful. 
            It allows you to control the TV.
        None - This indicates that pairing was unsuccessful."""

    tv_ip = "86.167.53.138"

    client = WebOSClient(tv_ip)
    client.connect()

    try:
        with open("store.json", "r") as f:
            store = json.load(f)
    except Exception as e:
        store = {}

    for status in client.register(store):
        if status == WebOSClient.PROMPTED:
            speech.say(f"Please accept the prompt on the TV.")
        elif status == WebOSClient.REGISTERED:
            pass

    with open("store.json", "w") as f:
        json.dump(store, f)

    return client
    
    
def notify(client: WebOSClient, message: str) -> int:
    if not isinstance(client, WebOSClient):
        return -1
    
    system = SystemControl(client)
    
    system.notify(f"J.A.R.V.I.S - {message.strip()}")
    return 0


def system_control(client: WebOSClient, message: str) -> int:
    """
    This is designed to control things relating to the TV system.
    This is either: 
        - screen off
        - screen on
        - power off
    It can NOT power on the TV as the TV needs to be connected to the
    network in order for this to work, and when it is powered off it is
    not.
    
    Parameters:
        client: WebOSClient - The client that allows us to control the TV
        message: str - The command you want to execute.
    
    Returns:
        int - A 0 for success, a value < 0 for errors.
    """
    
    if not isinstance(client, WebOSClient):
        return -1

    system = SystemControl(client)

    commands: dict[str, Callable] = {
        "screen off": system.screen_off,
        "screen on": system.screen_on,
        "off": system.power_off
    }

    for command, action in commands.items():
        if command in message:
            action()
            return 0

    return 0


def media_control(client: WebOSClient, message: str) -> int:
    """
    This is designed to control things relating to the media on the TV.
    This is either: 
        - Volume Up / Down
        - Set Volume {VALUE}
        - Mute Volume
        - Play / Pause media
    
    Parameters:
        client: WebOSClient - The client that allows us to control the TV
        message: str - The command you want to execute.
    
    Returns:
        int - A 0 for success, a value < 0 for errors.
    """
    
    if not isinstance(client, WebOSClient):
        return -1

    media = MediaControl(client)

    if "volume" in message and "up" in message:
        media.volume_up()
        notify(client, "Volume turned up successfully")
        return 0
        
    if "volume" in message and "down" in message:
        media.volume_down()
        notify(client, "Volume turned down successfully")
        return 0
        
    if "volume" in message and "set" in message:
        volume: str = ""
        for char in message:
            if char.isnumeric():
                volume += char
        new_volume: int = int(volume)
        if new_volume > 100: new_volume = 100
        if new_volume < 0: new_volume = 0
        media.set_volume(new_volume)
        notify(client, f"Volume set to {new_volume} successfully")
        return 0

    if "volume" in message and "mute" in message:
        media.mute(True)
        notify(client, "Volume Muted")
        return 0
        
    if "volume" in message and "unmute" in message:
        media.mute(False)
        notify(client, "Volume Unmuted")
        return 0

    if any(word in message for word in ["play", "resume", "continue"]):
        media.play()
        notify(client, "Media Resumed")
        return 0

    if any(word in message for word in ["pause", "stop"]):
        media.pause()
        notify(client, "Media Paused")
        return 0

    return 0


def appication_control(client: WebOSClient, message: str) -> int:
    """
    This is designed to control things relating to TV applications.
    This is: 
        - launch {APPLICATION}
    
    Parameters:
        client: WebOSClient - The client that allows us to control the TV
        message: str - The command you want to execute.
    
    Returns:
        int - A 0 for success, a value < 0 for errors.
    """

    if not isinstance(client, WebOSClient):
        return -1

    app: ApplicationControl = ApplicationControl(client)

    message = message.replace("launch", "", 1).replace("open", "", 1)
    message = message.replace("on tv", "", 1)
    app_list = app.list_apps()

    apps_to_open = [x for x in app_list if x["title"].lower() in message]
    if len(apps_to_open) >= 1:
        app_to_open = apps_to_open[0]
    else:
        speech.say(f"No Valid App found")
        return -1

    speech.say(f"Opening {app_to_open['title']} on your TV")
    app.launch(app_to_open)
    notify(client, f"Opened {app_to_open['title']}")
    return 0


def tv_control(client: WebOSClient, message: str) -> int:
    """
    This is designed to control things relating to live TV.
    This is either: 
        - Channel Up
        - Channel Down
        - Set Channel {CHANNEL NUMBER}
    
    Parameters:
        client: WebOSClient - The client that allows us to control the TV
        message: str - The command you want to execute.
    
    Returns:
        int - A 0 for success, a value < 0 for errors.
    """

    if not isinstance(client, WebOSClient):
        return -1

    inp = InputControl(client)
    tv = TvControl(client)

    num_buttons: dict[str, Callable] = {
        "1": inp.num_1,
        "2": inp.num_2,
        "3": inp.num_3,
        "4": inp.num_4,
        "5": inp.num_5,
        "6": inp.num_6,
        "7": inp.num_7,
        "8": inp.num_8,
        "9": inp.num_9,
        "0": inp.num_0
    }

    if "up" in message:
        tv.channel_up()
        notify(client, "Channel Increased")
        return 0

    if "down" in message:
        tv.channel_down()
        notify(client, "Channel Decreased")
        return 0

    if "channel" in message:
        for char in message:
            if char.isnumeric():
                num_buttons[str(char)]()
        notify(client, "Channel changed")

        return 0
    
    if "type " in message:
        inp.type(message.replace("type ", "", 1))
        return 0

    return 0
        
