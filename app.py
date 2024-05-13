import streamlit as st
from PIL import Image
import numpy as np
import cv2
from tensorflow.keras.models import load_model


# Setting up the page
st.set_page_config(page_title="CT Scan Image Viewer", page_icon="🖼️", layout="wide", initial_sidebar_state="expanded")

# Custom background with HTML and CSS
video_background_html = """
<style>
#root {overflow: visible;}
#bgVideo {position: fixed; top: 0; left: 0; right: 0; bottom: 0; width: 100vw; height: 100vh; object-fit: cover; z-index: -1;}
.stApp {z-index: 1; background: transparent;}
.content {padding: 1rem; color: #fff;}
</style>
<video id="bgVideo" autoplay loop muted playsinline>
    <source src="https://cdn.pixabay.com/video/2021/04/04/69951-538962240_large.mp4" type="video/mp4">
    Your browser does not support HTML5 video.
</video>
"""
st.markdown(video_background_html, unsafe_allow_html=True)

# Sidebar for user inputs
with st.sidebar:
    st.header("About")
    st.info("Upload and analyze CT scan images with respect to surgical needs.")
    processing_option = st.selectbox("Choose analysis type:", ["Type 1", "Type 2", "Type 3"])
    st.text_area("Notes", "Enter notes here...")

# Main page content
st.title('CT Scan Image Viewer')
uploaded_file = st.file_uploader("Upload your CT scan image", type=["png", "jpg", "jpeg"])

# Attempt to load the model
try:
    model_path = "/content/Pretrained Model.h5"  # Adjust path as necessary
    model = load_model(model_path)
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

# Processing uploaded files
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded CT Scan', use_column_width=True)
    with st.spinner('Processing image...'):
        img = cv2.imdecode(np.frombuffer(uploaded_file.getvalue(), np.uint8), cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (128, 128)) / 255.0
        img = img.reshape(-1, 128, 128, 1)
        prediction = model.predict(img)
        result = 'Surgery Needed' if prediction[0][0] > 0.5 else 'No Surgery Needed'
        time.sleep(5)  # Simulate processing time
    st.success(f"Result: {result}")
else:
    st.info("Please upload an image to proceed.")
