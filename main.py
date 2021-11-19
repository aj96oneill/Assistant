"""
Install the following (pip3 install _) :
- pyttsx3 (text to speech)
- speechRecognition (robot listener) (might need to brew install portAudio and then pip3 install pyAudio)
- pywhatkit (adv control of a browser)
- wikipedia (wiki data)
- pyjokes
"""
import speech_recognition as sr
import pyttsx3
import pywhatkit as kit
from datetime import datetime
import time
import wikipedia
import pyjokes
import threading

#Put in settings JSON
# current_voice = 0
# ASSISTENT_NAME = 'apple'
# WAIT_TIME = 1

listener = sr.Recognizer()
engine = pyttsx3.init()
current_voice = 0
engine.setProperty('voice', engine.getProperty('voices')[current_voice].id)
ASSISTENT_NAME = 'apple'
WAIT_TIME = 1



def talk(text):
    print(text)
    engine.say(text)
    engine.runAndWait()


def take_command():
    command = 'DummyString'
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source, duration=WAIT_TIME)
        print('listening...')
        voice = listener.listen(source)
    try:
        text = listener.recognize_google(voice)
        text = text.lower()
        if ASSISTENT_NAME in text:
            command = text.replace(ASSISTENT_NAME, '')
    except:
        print("Couldn't recognize what was said")
    return command

def take_response():
    command = 'DummyString'
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source, duration=WAIT_TIME)
        print('listening...')
        voice = listener.listen(source)
    try:
        text = listener.recognize_google(voice)
        text = text.lower()
        command = text
    except:
        print("Couldn't recognize what was said")
    return command

def send_text(text):
    #target needs to be a phone number +1... and text should also be a string
    now = datetime.now()
    hour = int(now.strftime("%H"))
    minute = int(now.strftime("%M"))+1
    if minute == 0:
        hour += 1
    kit.sendwhatmsg("+1...", text, hour, minute)

def change_voice():
    voices = engine.getProperty('voices')
    leaveLoop = False
    talk("Which assistent would you like to switch to")
    names = []
    for voice in voices:
        if 'en_US' in voice.languages[0]:
            if(voice.name != voices[current_voice].name):
                names.append(voices.index(voice))
    for name in names:
        engine.say(voices[name].name)
        print(voices[name].name)
        if names.index(name) != len(names)-1:
            engine.say("or")
            print("or")
    engine.runAndWait()
    while not leaveLoop:
        response = take_response()
        print("Response: "+ response)
        if "dummystring" in response:
            talk("Please try saying a name again")
        elif "nevermind" in response or "cancel" in response or "stop" in response:
            leaveLoop = True
        else:
            for name in names:
                if voices[name].name.lower() in response:
                    leaveLoop = True
                    engine.setProperty('voice', voices[name].id)
                    talk("Hello, I am your new assistent")
                    break

def change_volume(change_text):
    volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    if "percent" in change_text:
        #find what percent is being said
        #volume = ## / 100
        pass
    elif "eleven" in change_text:
        volume = .11
    #more elifs for different numbers
    elif "lower" in change_text:
        volume = volume - .2
        if volume < 0: volume = 0
    elif "raise" in change_text:
        volume = volume - .2
        if volume > 1: volume = 1
    else:
        talk("What level should the volume be set to")
        response = take_response()
        change_volume(response)
    engine.setProperty('volume',volume)

def change_name():
    pass

def timer(timer_length):
    # def square():
    # start_time = time.time()
    # x = int(input('Enter number: '))
    # squared = x*x
    # print('Square is: %s ' %squared)
    # print('Time elapsed: %s seconds' %(time.time() - start_time))
    #
    #
    # set_thread = threading.Thread(target=square) #set Thread() to run on square() function
    #
    # set_thread.start()
    pass

def run_assistant():
    command = take_command()
    print("CMD: "+command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        kit.playonyt(song)
    elif 'what time' in command:
        time = datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        talk(info)
    elif 'date' in command:
        talk('sorry, I have a headache')
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'volume' in command:
        change_volume(command.replace('volume', ''))
    elif 'change' in command and 'voice' in command:
        change_voice()
    elif 'turn off' in command:
        talk("good night")
        return False
    else:
        talk('Please say the command again.')
    return True

# background listening example?:
# # this is called from the background thread
# def callback(recognizer, audio):
#     # received audio data, now we'll recognize it using Google Speech Recognition
#     try:
#         # for testing purposes, we're just using the default API key
#         # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
#         # instead of `r.recognize_google(audio)`
#         print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
#     except sr.UnknownValueError:
#         print("Google Speech Recognition could not understand audio")
#     except sr.RequestError as e:
#         print("Could not request results from Google Speech Recognition service; {0}".format(e))
#
# r = sr.Recognizer()
# m = sr.Microphone()
# with m as source:
#     r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
#
# # start listening in the background (note that we don't have to do this inside a `with` statement)
# stop_listening = r.listen_in_background(m, callback)
# # `stop_listening` is now a function that, when called, stops background listening
#
# # do some unrelated computations for 5 seconds
# for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things
#
# # calling this function requests that the background listener stop listening
# stop_listening(wait_for_stop=False)
#
# # do some more unrelated things
# while True: time.sleep(0.1)  # we're not listening anymore, even though the background thread might still be running for a second or two while cleaning up and stopping
if __name__ == '__main__':
    while run_assistant(): pass
