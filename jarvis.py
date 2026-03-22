# jarvis.py
import os
import struct
import pvporcupine
import pyaudio
import sounddevice as sd
import soundfile as sf
import whisper
import pyttsx3
from dotenv import load_dotenv
from openai import OpenAI

# === LOAD ENVIRONMENT VARIABLES ===
load_dotenv()

# === SETUP KEYS ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PICOVOICE_ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# === FUNCTION 1: Wake Word Detection ===
def detect_wake_word(keyword_path="jarvis.ppn"):
    porcupine = pvporcupine.create(
        access_key=PICOVOICE_ACCESS_KEY,
        keyword_paths=[keyword_path]
    )
    pa = pyaudio.PyAudio()
    stream = pa.open(rate=porcupine.sample_rate,
                     channels=1,
                     format=pyaudio.paInt16,
                     input=True,
                     frames_per_buffer=porcupine.frame_length)

    print("🎧 Listening for wake word ('Jarvis')...")

    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        result = porcupine.process(pcm)
        if result >= 0:
            print("✅ Wake word detected!")
            stream.stop_stream()
            stream.close()
            pa.terminate()
            return True


# === FUNCTION 2: Record Audio ===
def record_audio(filename="command.wav", duration=5, samplerate=16000):
    print("🎙️ Listening for your command...")
    data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    sf.write(filename, data, samplerate)
    return filename


# === FUNCTION 3: Speech to Text (Local Whisper) ===
def transcribe_audio(audio_file):
    model = whisper.load_model("base")  # or "small"/"medium"/"large"
    print("🧠 Transcribing with Whisper (local)...")
    result = model.transcribe(audio_file)
    return result["text"]


# === FUNCTION 4: Gemini Response ===
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gpt(text):
   model = genai.GenerativeModel("models/gemini-2.5-flash")
   response = model.generate_content(text)
   return response.text



# === FUNCTION 5: Text to Speech ===
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)  # Adjust speaking speed
    engine.say(text)
    engine.runAndWait()


# === MAIN LOOP ===
if __name__ == "__main__":
    while True:
        detected = detect_wake_word("/Users/harshitmehra/Desktop/Python/jarvis.ppn")

        if detected:
            audio_file = record_audio()
            text = transcribe_audio(audio_file)
            print(f"🗣️ You said: {text}")
            reply = ask_gpt(text)
            print(f"🤖 Jarvis: {reply}")
            speak(reply)
