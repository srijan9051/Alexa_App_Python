import requests
import re
import webbrowser
import pyttsx3
import speech_recognition as sr

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_first_youtube_video_url(query):
    search_url = f"https://www.youtube.com/results?search_query={query}"
    response = requests.get(search_url)
    html = response.text
    
    # Using regex to find the first video URL
    match = re.search(r"\"videoId\":\"(.*?)\"", html)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"
    return None

def process_command(command):
    if "open google" in command.lower():
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in command.lower():
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open gmail" in command.lower():
        speak("Opening Gmail")
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
    elif "open github" in command.lower():
        speak("Opening GitHub")
        webbrowser.open("https://github.com/")
    elif "open portfolio" in command.lower():
        speak("Opening your portfolio")
        webbrowser.open("https://srijansportfollio.online")
    elif "open chatbot" in command.lower():
        speak("Opening chat g p t")
        webbrowser.open("https://chatgpt.com/")
    elif command.lower().startswith("play"):
        query = command.replace("play ", "", 1)
        speak(f"Playing {query}")
        video_url = get_first_youtube_video_url(query)
        if video_url:
            webbrowser.open(video_url)
        else:
            speak("I couldn't find any videos for that query.")
    elif command.lower().startswith("open"):
        remaining = command.replace("open ", "", 1)
        query=f"https://www.youtube.com/results?search_query={remaining}"
        speak(f"opening {remaining}")
        webbrowser.open(query)
    elif command.lower().startswith("search"):
        remaining=command.replace("search ","",1)
        query=f"https://www.google.com/search?q={remaining}"
        speak(f"searching {remaining}")
        webbrowser.open(query)

if __name__ == "__main__":
    speak("Initializing Jarvis")
    while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=3)
            word = recognizer.recognize_google(audio)
            if "alexa" in word.lower():
                speak("Yes sir...")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source, timeout=3)
                command = recognizer.recognize_google(audio)
                process_command(command)
                
                
        except Exception as e:
            print(f"Error: {e}")