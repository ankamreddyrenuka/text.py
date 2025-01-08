import streamlit as st
import pytesseract
from PIL import Image
import pyttsx3
import tempfile
import base64

# Simplification function (you can enhance this with more complex rules)
def simplify_text(text):
    word_replacements = {
        "difficult": "hard",
        "utilize": "use",
        "comprehend": "understand",
        "nevertheless": "but",
        "assistance": "help"
    }
    
    words = text.split(" ")
    simplified_words = [
        word_replacements.get(word.lower(), word) if word.lower() in word_replacements else word
        for word in words
    ]
    return " ".join(simplified_words)

# Function to convert text to speech using a basic approach
def text_to_speech(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    
    # Save speech to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        engine.save_to_file(text, temp_file.name)
        engine.runAndWait()
        
        # Convert the file to base64
        with open(temp_file.name, "rb") as f:
            audio_data = f.read()
            base64_audio = base64.b64encode(audio_data).decode("utf-8")
            
    return base64_audio

# Function to extract text from image using OCR
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Main function to create the Streamlit interface
def main():
    st.title("Text Simplifier with OCR")
    
    # Image uploader
    uploaded_image = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
    
    if uploaded_image is not None:
        # Open image using PIL
        image = Image.open(uploaded_image)
        
        # Extract text from the image
        extracted_text = extract_text_from_image(image)
        
        if extracted_text:
            st.subheader("Extracted Text")
            st.write(extracted_text)
            
            # Simplify the extracted text
            simplified = simplify_text(extracted_text)
            st.subheader("Simplified Text")
            st.write(simplified)
            
            # Text-to-speech functionality
            if st.button("Read Simplified Text"):
                audio_base64 = text_to_speech(simplified)
                st.audio(f"data:audio/mp3;base64,{audio_base64}", format="audio/mp3")
        else:
            st.error("No text could be extracted from the image.")
    
    # Instructions
    st.sidebar.header("How It Works")
    st.sidebar.write("""
        - Image Upload: Upload an image containing text.
        - Extract & Simplify: The text in the image will be extracted and simplified into easier language.
        - Text-to-Speech: Press the "Read Simplified Text" button to hear the simplified text.
    """)

if __name__== "__main__":
    main()


