import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import random

#  TEXT TO SPEECH 
engine = pyttsx3.init()
engine.setProperty("rate", 175)

def speak(text):
    print("🤖 Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# SPEECH TO TEXT 
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print("🗣️ You said:", command)
        return command
    except:
        return ""

#  COMMAND HANDLER 
def run_command(command):

    # ⏰ TIME
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"Current time is {current_time}")

    # 📅 DATE
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today is {current_date}")

    # 🌐 OPEN WEBSITES
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")

    elif "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")

    elif "open spotify" in command:
        os.system("open -a Spotify")
        speak("Opening Spotify")

    # 🎵 PLAY MUSIC (FIXED)
    elif "play music" in command:
        music_dir = os.path.expanduser("~/Desktop/Music")

        try:
            songs = [s for s in os.listdir(music_dir) if s.endswith(('.mp3', '.wav', '.m4a'))]

            if not songs:
                speak("No songs found in your music folder")
                return

            song = random.choice(songs)
            full_path = os.path.join(music_dir, song)

            print("Playing:", full_path)
            os.system(f"open '{full_path}'")

            speak("Playing music")

        except Exception as e:
            print(e)
            speak("Error playing music")

    # 👋 GREETING
    elif "hello" in command:
        speak("Hello Harshit  😎")

    # ❌ EXIT
    elif "exit" in command or "stop" in command:
        speak("Goodbye bhai 👋")
        exit()

    # 🤖 UNKNOWN
    else:
        speak("I didn't understand that")

#  MAIN LOOP 
if __name__ == "__main__":
    speak("Jarvis is online")

    while True:
        command = listen()

        if command.strip() != "":
            run_command(command)
