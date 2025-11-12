# MRI Report Generator

An intelligent web application that automatically generates comprehensive MRI reports from PDF documents using AI-powered text summarization, image search, and text-to-speech capabilities.

## 📋 Overview

The MRI Report Generator is a Flask-based web application that processes medical MRI report PDFs and transforms them into accessible, multimedia presentations. It extracts text from PDF reports, generates AI-powered summaries, fetches relevant medical images, and creates audio narrations in multiple languages.

## ✨ Features

- **📄 PDF Text Extraction**: Automatically extracts text content from uploaded MRI report PDFs
- **🤖 AI-Powered Summarization**: Uses BART (facebook/bart-large-cnn) transformer model for intelligent text summarization
- **🔍 Smart Keyword Extraction**: Identifies key medical terms from the report
- **🖼️ Automated Image Search**: Fetches relevant medical images using Google Custom Search API
- **🔊 Text-to-Speech**: Converts summaries to audio in multiple languages (English & Hindi)
- **🎥 Video Generation**: Creates video presentations combining images and audio
- **🌐 Multi-language Support**: Supports English and Hindi language options
- **🧹 Text Cleaning**: Removes unwanted signatures and metadata from reports

## 🛠️ Technologies Used

- **Backend**: Flask (Python Web Framework)
- **AI/ML**: 
  - Transformers (Hugging Face) - BART model for summarization
  - PyTorch - Deep learning framework
- **PDF Processing**: PyMuPDF (fitz)
- **Text-to-Speech**: gTTS (Google Text-to-Speech)
- **Translation**: deep-translator (Google Translator)
- **Image Processing**: Pillow, OpenCV (moviepy)
- **Web Scraping**: requests
- **Others**: Werkzeug for file handling

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Custom Search API Key
- Google Custom Search Engine ID

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/MEKALA-JASWANTH/MRI-Report-Generator.git
   cd MRI-Report-Generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**
   
   Open `app.py` and update your API credentials:
   ```python
   API_KEY = 'YOUR_GOOGLE_API_KEY'
   CSE_ID = 'YOUR_CUSTOM_SEARCH_ENGINE_ID'
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   
   Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## 📖 Usage

1. **Upload MRI Report**: Click on the upload button and select an MRI report PDF file
2. **Select Language**: Choose between English or Hindi for the audio output
3. **Submit**: Click submit to process the report
4. **View Results**: The application will display:
   - Summarized report text
   - Relevant medical images
   - Audio narration
   - Generated video

## 📁 Project Structure

```
MRI-Report-Generator/
│
├── app.py                  # Main Flask application
├── main.py                 # Alternative entry point
├── utils.py                # Utility functions (keyword extraction, image search)
├── video_generator.py      # Video generation functionality
├── merger.py               # File merging utilities
├── test.py                 # Testing scripts
├── requirements.txt        # Python dependencies
├── my_project.zip          # Project archive
│
├── static/
│   ├── uploads/            # Uploaded PDF files
│   └── summary.mp3         # Generated audio files
│
└── templates/
    └── index.html          # Web interface
```

## 🔑 Key Components

### 1. Text Extraction (`extract_text_from_pdf`)
Extracts text content from PDF files using PyMuPDF library.

### 2. Text Cleaning (`clean_unwanted_text`)
Removes unnecessary signatures, dates, and metadata using regex patterns.

### 3. AI Summarization (`summarize_locally`)
Uses Facebook's BART-large-CNN model to generate concise summaries (100-250 words).

### 4. Keyword Extraction (`extract_keywords`)
Identifies important medical terms from the summary for image search.

### 5. Image Search (`google_search_image`)
Fetches relevant medical images using Google Custom Search API.

### 6. Text-to-Speech (`text_to_speech`)
Converts text to audio using gTTS with support for multiple languages.

### 7. Video Generation (`generate_video`)
Combines images and audio to create an educational video.

## 📚 Dependencies

```
Flask==3.0.0
Werkzeug==3.0.1
fitz==0.0.1.dev2
PyMuPDF==1.23.8
transformers==4.36.0
torch==2.1.2
gtts==2.5.0
Pillow==10.1.0
moviepy==1.0.3
requests==2.31.0
keybert==0.8.3
google-translator==0.1
deep-translator==1.11.4
numpy==1.26.2
```

## 🔐 API Configuration

To use the Google Custom Search feature, you need to:

1. **Get a Google API Key**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable "Custom Search API"
   - Create credentials (API Key)

2. **Create a Custom Search Engine**:
   - Visit [Google Custom Search Engine](https://cse.google.com/)
   - Create a new search engine
   - Copy the Search Engine ID (CSE_ID)

## 🚀 Future Enhancements

- [ ] Support for DICOM image processing
- [ ] Integration with more AI models for better accuracy
- [ ] User authentication and report history
- [ ] Export reports in multiple formats (PDF, DOCX)
- [ ] Real-time collaboration features
- [ ] Mobile application
- [ ] Support for more languages
- [ ] Cloud deployment (AWS, Azure, GCP)

## 🐛 Known Issues

- Large PDF files may take longer to process
- Video generation requires sufficient disk space
- Google API has daily request limits

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**MEKALA JASWANTH**

- GitHub: [@MEKALA-JASWANTH](https://github.com/MEKALA-JASWANTH)
- Repository: [MRI-Report-Generator](https://github.com/MEKALA-JASWANTH/MRI-Report-Generator)

## 🙏 Acknowledgments

- Hugging Face for the Transformers library
- Google for Text-to-Speech and Custom Search APIs
- Flask community for the excellent web framework
- All contributors and users of this project

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

⭐ If you find this project useful, please consider giving it a star on GitHub!
