import requests
import re
import webbrowser
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import chatbot

recognizer = sr.Recognizer()
engine = pyttsx3.init()
apikey="your news api key"


def speak(text):
    tts=gTTS(text=text,lang='en',slow=False)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove('temp.mp3')


def get_first_youtube_video_url(query):
    search_url = f"https://www.youtube.com/results?search_query={query}"
    response = requests.get(search_url)
    html = response.text
    
  
    match = re.search(r"\"videoId\":\"(.*?)\"", html)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"
    return None

def refine_text(text):
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    return cleaned_text

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
    elif "news" in command.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apikey={apikey}")
        if r.status_code==200:
            data=r.json()
            articles=data.get('articles',[])

            for article in articles:
                speak(article['title'])
    else:
        text=command.lower()
        answer=chatbot.answer_anything(text)
        answer=refine_text(answer)
        speak(answer)

if __name__ == "__main__":
    speak("Hi srijan I am your assistent alexa")
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
            
                #print(command)
                
        except Exception as e:
            print(f"Error: {e}")