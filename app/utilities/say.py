import pyttsx3


def speak(text):
    # print(f"Saying: {text}")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    del engine

# speak("Text to speech module initialized.")
# speak("Ready to receive text.")
