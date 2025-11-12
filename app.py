import os
import fitz
import re
from flask import Flask, render_template, request, redirect, url_for
from gtts import gTTS
from transformers import pipeline
from utils import extract_keywords, google_search_image, download_images
from video_generator import generate_video
from deep_translator import GoogleTranslator

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

API_KEY = 'AIzaSyCmVoVbMIEUaARPCyKK5t_6DXLsCljKKYI'
CSE_ID = '26565ead217784ed2'

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def clean_unwanted_text(text):
    patterns_to_remove = [
        r"Thank you for your kind referral.*",
        r"-Electronically Signed by:.*",
        r"On \d{2}/\d{2}/\d{4}.*",
    ]
    for pattern in patterns_to_remove:
        text = re.sub(pattern, '', text, flags=re.DOTALL)
    text = re.sub(r'\n\s*\n', '\n\n', text).strip()
    return text

def summarize_locally(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=250, min_length=100, do_sample=False)
    return summary[0]['summary_text']

def text_to_speech(text, l, filename="summary.mp3"):
    if l == "hi":
        text = GoogleTranslator(source='auto', target='hi').translate(text)

    tts = gTTS(text, lang=l)
    filepath = os.path.join('static', filename)
    tts.save(filepath)
    return filepath

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['pdf']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            report_text = extract_text_from_pdf(file_path)
            cleaned_text = clean_unwanted_text(report_text)
            summary = summarize_locally(cleaned_text)
            keywords = extract_keywords(summary)
            image_paths = []

            for keyword in keywords:
                img_url = google_search_image(keyword, API_KEY, CSE_ID)
                img_path = download_images(img_url)
                image_paths.append(img_path)

            language = request.form.get('language', 'en')
            audio_path = text_to_speech(summary, language,"summary.mp3")

            video_path = generate_video()

            return render_template('index.html', summary=summary, audio=audio_path, video=video_path, images=image_paths)

    return render_template('index.html', summary=None)

if __name__ == '__main__':
    app.run(debug=True)
