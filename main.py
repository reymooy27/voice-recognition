import speech_recognition as sr
import pyaudio
import webbrowser as wb
import google.generativeai as genai
import pyttsx3
from selenium import common
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import threading
import subprocess

API_KEY = "AIzaSyDg7CrgXhz8a79-GbX_P_IBeHV7sX2Xj78"

APP = {
    "vlc player" :"/Program Files (x86)/VideoLAN/VLC/vlc.exe",
    "spotify": "C:/Program Files/Spotify/spotify.exe",
    "steam game": "C:/Program Files (x86)/Steam/steam.exe",
}

#setup selenium
# options = webdriver.EdgeOptions()
# options.accept_insecure_certs = True
# options.add_experimental_option("detach", True)
# options.add_argument("--disable-notifications")
# options.add_argument("user-data-dir=/Users/user/AppData/Local/Google/Chrome/User Data")
# options.add_argument("profile-directory=Default")
# options.add_argument("profile-directory=Profile 1")
browser = None


#init speech recognition
engine = pyttsx3.init()

#text to speech function
def speak(text):
    engine.say(text)
    engine.runAndWait()

def voice_recognition():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)

            try:
                #TODO: ganti TTS enginenya ke yg lebih baik
                audio = recognizer.listen(source, phrase_time_limit=10)
                text = recognizer.recognize_google(audio, language="id-ID")

                if "input" in text.lower():
                    text = input("Input text: ")

                #ini sebenarnya untuk scroll tiktok
                #belum jadi kalau youtube short
                #problemnya kalau ada kata next perintah yang lain gak jalan

                # if "next" in text.lower() or "skip" in text.lower() or "berikutnya" in text.lower():
                #     print("next ->")
                #     ActionChains(browser).scroll_by_amount(0,700).perform()
                #     continue

                # if "back" == text.lower():
                #     browser.back()

                print(f"You : {text}")

                reply = get_reply(text)

                print(f"AI : {reply}")

                # text to speech
                #TODO: buat supaya tidak perlu menunggu / tidak blocking next command
                speak(reply)


            except sr.UnknownValueError:
                print("Waiting for command")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}\n")


def get_reply(text):
    #TODO: ganti ke AI model yg lebih baik
    #for now gemini karena gratis
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = ""


    #cek kalau ada perintah buka or open website
    if "buka" in text.lower() or "open" in text.lower():
        global browser
        if browser is None:
            browser = webdriver.Edge();

        # for text in APP:
        #     if text in text.lower():
        #         subprocess.run(APP[text])
        #         continue

        response = model.generate_content("i want you to directly provide the link to the app or website that mentioned in this, : " + text + "for example, open youtube then give like https://youtube.com, do not provide any other text just the link in one line")
        if response.text[:5] != "https" or response.text[:4] != "http":
            return "No link found"

        if "new tab" in text.lower() or "tab baru" in text.lower():

            browser.switch_to.new_window("tab")

        browser.get(response.text)

    #untuk search
    if "search" in text.lower() or "cari" in text.lower():
        if browser is None:
            browser = webdriver.Edge();

        if "new tab" in text.lower() or "tab baru" in text.lower():

            browser.switch_to.new_window("tab")

        browser.get("https://www.google.com/search?q=" + text.replace("search", "").strip())

    response = model.generate_content("""You have the persona of a Jarvis like in Iron Man Movie, 
    Give output in plain text, without any symbol like ** for example, give short answer,""" + text)


    return response.text

if __name__ == "__main__":
    voice_recognition()
