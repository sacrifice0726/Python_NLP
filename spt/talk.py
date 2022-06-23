

def text_to_speech(text):
    import pyttsx3 
    s = pyttsx3.init()
    s.setProperty('voice','zh') 
    data = text
    s.say(data) 
    s.runAndWait() 