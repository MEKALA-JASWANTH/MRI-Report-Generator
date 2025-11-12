import fitz
import re
from gtts import gTTS
from transformers import pipeline
from utils import extract_keywords,google_search_image,download_images
from video_generator import generate_video
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

def text_to_speech(text, filename="summary.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    print(f"Audio summary saved as {filename}")

# === EXECUTION ===
file_path = 'MRI OF THE CERVICAL SPINE WO CONTRAST.pdf'
report_text = extract_text_from_pdf(file_path)
cleaned_text = clean_unwanted_text(report_text)

# Summarize the report
summary = summarize_locally(cleaned_text)
print("\nSUMMARY:\n", summary)
keywords = extract_keywords(summary)
for i in keywords:
    image = google_search_image(i, API_KEY, CSE_ID)
    download_images(image)
# Generate the audio file
text_to_speech(summary, "mri_summary.mp3")
generate_video()