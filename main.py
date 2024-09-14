from datetime import datetime as dt
import os
import random
import subprocess
import sys
import time

import requests

import browser
import speech
import tv


class JARVIS:
    def __init__(self, user_name: str = 'Sir') -> None:
        self.user_name = user_name
        self.date = dt.now().strftime("%A, %B %d, %Y")
        self.TV_client = None

    def exec_command(self, command) -> None:
        if any(word in command for word in [
            "date",
            "time"
        ]):
            self.info(command)
            return
            
        if "search" in command:
            self.search(command.replace("search", "", 1))
            return

        if "what is" in command:
            browser.wikipedia_search(command.replace("what is", "", 1))
            return
            
        if "tv" in command:
            self.TV(command)
            return

        if "open" in command:
            browser.open_website(command.replace("open", "", 1))
            return

        if "light" in command:
            self.lights(command)
            return

        if any(word in command for word in [
            "single",
            "joke",
            "repeat after me",
            "thank"
        ]):
            self.fun(command)
        
        if any(word in command for word in [
            "goodbye",
            "bye",
            "exit",
            "close",
            "quit"
        ]):
            speech.say(f"Goodbye {self.user_name}")
            sys.exit()

        if "shut down" in command or "shutdown" in command:
            self.lights("off")
            self.TV("screen off")
            time.sleep(5)
            self.lights("on")
            self.TV("screen on")
            speech.say("Phew, that was scary.")
        


    def search(self, command: str) -> None:
        if "on wikipedia" in command:
            browser.wikipedia_search(command.replace("on wikipedia", "", 1))
            return
        
        if any(word in command for word in [
            "on duck duck go",
            "on duckduckgo"
        ]):
            browser.search(command.replace("on duckduckgo", "", 1).replace("on duck duck go", "", 1), 2)
            return

        if "on bing" in command:
            browser.search(command.replace("on bing", "", 1), 1)
            return

        if "on yahoo" in command:
            browser.search(command.replace("on yahoo", "", 1), 3)
            return

        if "on google" in command:
            browser.search(command.replace("on google", "", 1))
            return

        if "on youtube" in command:
            browser.search(command.replace("on youtube", "", 1), 4)
            return
            
        browser.search(command)


    def info(self, command: str) -> None:
        if "date" in command:
            speech.say(f"Today is {dt.now().strftime('%A, %d %B %Y')}")
            return

        if "time" in command:
            speech.say(f"It is currently {dt.now().strftime('%H:%M')} on {dt.now().strftime('%A, %d %B %Y')}")
            return


    def lights(self, command: str) -> None:
        light_on_trigger = "https://api-v2.voicemonkey.io/trigger?token=5ae64dd19d0232fadb94e07308ec9143_382e8951d293256059c4ca26f47fa06d&device=light-on-trigger"
        light_off_trigger = "https://api-v2.voicemonkey.io/trigger?token=5ae64dd19d0232fadb94e07308ec9143_382e8951d293256059c4ca26f47fa06d&device=light-off-trigger"

        if "on" in command:
            requests.get(light_on_trigger)
            speech.say("Light turned On")
            return
            
        if "off" in command:
            requests.get(light_off_trigger)
            speech.say("Light turned Off")
            return

        if "flash" in command:
            for _ in range(5):
                requests.get(light_off_trigger)
                time.sleep(5)
                requests.get(light_on_trigger)
                time.sleep(5)

        return
        

    def TV(self, command: str) -> None:
        if self.TV_client is None:
            self.TV_client = tv.connect()
            
        command = command.replace("on tv", "", 1)
        
        if any(word in command for word in [
            "on",
            "off"
        ]):
            tv.system_control(self.TV_client, command)
            return

        if any(word in command for word in [
            "volume",
            "mute",
            "play",
            "pause"
        ]):
            tv.media_control(self.TV_client, command)
            return

        if any(word in command for word in ["launch", "open"]):
            tv.appication_control(self.TV_client, command)
            return

        if "channel" in command:
            tv.tv_control(self.TV_client, command)
            return
        
        
    def fun(self, command: str) -> None:
        if "single" in command:
            # Say a random funny phrase
            speech.say(random.choice([
                "No, I'm in a relationship with your WIFI",
                "Yes, it's a bit lonely out here..."
            ]))
            return
        
        if "joke" in command:
            # Set the headers of return type and user agent
            headers = {
                'User-Agent': 'J.A.R.V.I.S',
                'Accept': 'application/json'
            }
            # Get the response (status code, joke)
            response = requests.get(
                "https://icanhazdadjoke.com/",
                headers=headers
            )
            # If it was a successful call...
            if response.status_code == 200:
                data = response.json() # Get the json from the response
                speech.say(data["joke"]) # Say the joke
            else:
                speech.say("Sorry, i encountered an error.")
            
            return

        if "repeat after me" in command:
            command = command.replace("repeat after me", "", 1)
            speech.say(command)
            return
        
        if "thank" in command: # Thanks or thank you
            speech.say(random.choice([
                "You're welcome",
                "You're very welcome",
                "My pleasure",
                "Always a pleasure to help",
                "Anything for you",
                "Happy i could be of help",
                "Don't mention it"
            ]))
        
        

model = JARVIS("Liam")

while True:
    subprocess.run(["cls"], shell=True)
    model.exec_command(speech.get_message())