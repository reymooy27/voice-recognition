import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
from selenium import webdriver
import pyautogui

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

#init text to speech engine
engine = pyttsx3.init()

#text to speech function
def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_reply(text):
    #TODO: ganti ke AI model yg lebih baik
    #for now gemini karena gratis
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = ""

    if "click" in text.lower() or "klik" in text.lower():
        pyautogui.click()
        return "Clicked"

    if "type" in text.lower() or "ketik" in text.lower():
        pyautogui.typewrite(text.replace("type", "").replace("ketik", "").strip())
        return "Typed"

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

        if "tiktok" in text.lower() or "tik tok" in text.lower():
            browser.get("https://www.tiktok.com/")
            return "Opened Tiktok"

        if "new tab" in text.lower() or "tab baru" in text.lower():
            browser.switch_to.new_window("tab")
            browser.get(response.text)
        else:
            browser.get(response.text)

        if response.text[:5] != "https" or response.text[:4] != "http":
            return "No link found"

        return "Opened"

    #untuk search
    if "search" in text.lower() or "cari" in text.lower():
        if browser is None:
            browser = webdriver.Edge();

        if "new tab" in text.lower() or "tab baru" in text.lower():
            browser.switch_to.new_window("tab")
            browser.get("https://www.google.com/search?q=" + text.replace("search", "").strip())
        else:
            browser.get("https://www.google.com/search?q=" + text.replace("search", "").strip())

        return "Searched" + text

    response = model.generate_content("""You have persona of a cool guy, you are using Bahasa Indonesia, Give output in plain text, without any symbol like ** for example, give short answer,""" + text)

    return response.text