from deep_translator import GoogleTranslator
from gtts import gTTS
import os

def text_to_speech(text, l, filename="summary.mp3"):
    if l == "hi":
        text = GoogleTranslator(source='auto', target='hi').translate(text)

    tts = gTTS(text, lang=l)
    filepath = os.path.join('static', filename)
    tts.save(filepath)
    return filepath

print(text_to_speech("Hello, how are you?", "hi", "summary.mp3"))
