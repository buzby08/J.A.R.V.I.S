from gtts import gTTS
import pygame
from pydub import AudioSegment
from pydub.playback import play
import string
import subprocess
import wave
import os
import pyttsx3
import speech_recognition as sr
import random


def say(message: str) -> int:
    """
    A function to say a given message.
    
    Parameters: 
        message: str - The message you want to say.
    
    Returns:
        int - A 0 for success, or a number < 0 for an error.
    """

    print("")
    print("J.A.R.V.I.S: " + message.strip())
    print("")
    
    engine = pyttsx3.init(driverName="sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", 145)
    engine.say(message.strip())
    engine.runAndWait()

    return 0


def play_audio(audio_file: str) -> None:
    """
    This procedure loads the audio file `audio_file` and plays
    its contents.

    Parametrs:
        audio_file: str - The path to the file you want to play

    Returns:
        None - This is a procedure
    """

    

    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass

    time.sleep(0.5)

    return



def get_message() -> str:
    """
    This is designed to get a message from the user, using the microphone.
        
    Returns:
        str - A string of the message.
    """
    
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
            try:
                raw_text = r.recognize_google(audio)
                checked_text = check_text(raw_text)

                if not checked_text:
                    continue

                else:
                    return checked_text
                
            except:
                continue


def check_text(text: str) -> str:
    text = text.strip().lower()

    if "jarvis" not in text:
        return ""
    
    index = text.index("jarvis")
    return text[index+6:]


def remove_punctuation(message: str) -> str:
    """
    This function is designed to remove any unnecessary characters from
    a string. 
    
    Parameters:
        message: str - The message you want to abstract.
    
    Returns:
        str - The abstracted string.
    """
    
    message = str(message)
    new_message: str = ""
    for char in message:
        if char in string.ascii_letters+' ':
            new_message += char
        if char.isnumeric():
            new_message += char

    return new_message.lower()


def write_log(error_message: Exception) -> None:
    if os.stat("log.txt").st_size > 5_000:
        with open("log.txt", "w") as f:
            f.write("")

    with open("log.txt", "a") as f:
        f.write(str(error_message) + "\n\n")
    return


def convert_to_wav(input_file: str, output_file: str) -> None:
    if not output_file.endswith('.wav'):
        raise ValueError("The output file must be a .wav file.")

    try:
        audio = AudioSegment.from_mp3(input_file)

        audio.export(output_file, format="wav")
    
    except Exception as e:
        print("I'm having trouble right now, please try again later.")
        return
