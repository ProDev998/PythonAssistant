import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

last_interaction_time = time.time()  # Track the time of last interaction

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis Sir. Please tell me how may I help you")

def takeCommand():
    global last_interaction_time
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        last_interaction_time = time.time()  # Update last interaction time
        if "max" in query.lower():  # Check for wake command
            wishMe()
            return ""
        return query
    except Exception as e:
        print("Say that again please...")
        return ""

def search_wikipedia(query):
    speak('Searching Wikipedia...')
    query = query.replace("wikipedia", "")
    results = wikipedia.summary(query, sentences=2)
    speak("According to Wikipedia")
    print(results)
    speak(results)

if __name__ == "__main__":
    wishMe()
    while True:
        if time.time() - last_interaction_time > 15:  # Check if there's been no interaction for 15 seconds
            print("Going back to sleep...")
            speak("Going back to sleep...")
            last_interaction_time = time.time()  # Reset last interaction time
            time.sleep(1)
            continue

        query = takeCommand().lower()

        if query == "":
            continue

        if 'wikipedia' in query:
            search_wikipedia(query)
        elif 'search' in query:
            query = query.replace('search', '')
            google_search_url = f"https://www.google.com/search?q={query}"
            webbrowser.open(google_search_url)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        elif 'open code' in query:
            codePath = "C:\\Users\\Haris\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)