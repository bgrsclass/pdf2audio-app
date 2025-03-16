import streamlit as st
import pyttsx3
import PyPDF2
from io import BytesIO
import tempfile

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"

# Function to convert text to speech and save it as a file
def text_to_speech(text, language):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 125)  # Adjust speed
    
    voice_found = False
    for voice in voices:
        # Use Indian English voice for Hindi+English mix
        if ('en_in' in voice.id or 'hindi' in voice.name.lower() or 'english' in voice.name.lower()):
            engine.setProperty('voice', voice.id)
            voice_found = True
            break

    if not voice_found:
        engine.setProperty('voice', voices[0].id)  # Default fallback

    # Improve pronunciation for Hindi+English mix
    formatted_text = text.replace(".", ". ").replace(",", ", ")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        audio_path = temp_audio.name

    engine.save_to_file(formatted_text, audio_path)
    engine.runAndWait()
    return audio_path



# Streamlit UI
st.title("PDF to Speech Converter")

# File uploader for PDF
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if pdf_file:
    extracted_text = extract_text_from_pdf(pdf_file)
    st.text_area("Extracted Text", extracted_text, height=200)
    
    if extracted_text:
        language = st.selectbox("Select Language", ["English", "Hindi", "Telugu", "Odia", "Bengali"])
        
        if st.button("Convert to Speech"):
            audio_file_path = text_to_speech(extracted_text, language)
            
            with open(audio_file_path, "rb") as file:
                st.audio(file, format="audio/mp3")
                st.download_button(label="Download Speech", data=file, file_name="speech.mp3", mime="audio/mpeg")
                st.success("Speech conversion completed!")
