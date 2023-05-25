import json, os, requests
import pyttsx3, pyaudio, vosk

tts = pyttsx3.init('sapi5')
voices = tts.getProperty('voices')
tts.setProperty('voices', 'en')

for voice in voices:
    print(voice.name)
    if voice.name == 'Microsoft Zira Desktop - English (United States)':
        tts.setProperty('voice', voice.id)

model = vosk.Model('vosk-model-small-en-us-0.15')
record = vosk.KaldiRecognizer(model, 16000)
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=16000,
                 input=True,
                 frames_per_buffer=8000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']


def speak(say):
    tts.say(say)
    tts.runAndWait()

def save(word):  
    response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    data = response.json()
    with open("data.txt", "w") as f:
        json.dump(data, f)
    print("Saved to a file data.txt")

def meaning(word):
    response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    data = response.json()
    print(data[0]['meanings'][0]['definitions'][0]['definition'])
    speak(data[0]['meanings'][0]['definitions'][0]['definition'])
        
def link(word):
    response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    data = response.json()
    print(data[0]['sourceUrls'][0])

def example(word):
    response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    data = response.json()
    print(data[0]['meanings'][0]['definitions'][0]['example'])
    speak(data[0]['meanings'][0]['definitions'][0]['example'])

for text in listen():
    if 'find' in text:
        term = text.split("find ")[1]
        response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{term}')
        data = response.json()
        print(data['message'])
    elif text == 'meaning':
        meaning(term)
    elif text == 'example':
        example(term)
    elif text == 'save':
        save(term)
    elif text == 'link':
        link(term)
    elif text == 'exit':
        break
    else:
        print('The command is not recognized')
