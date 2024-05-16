!pip install streamlit tensorflow pillow

import os
import cv2
import numpy as np
import streamlit as st
from PIL import Image
from tensorflow.keras.models import load_model

def is_image_file(filename):
    valid_extensions = ['.png', '.jpg', '.jpeg']
    return any(filename.lower().endswith(ext) for ext in valid_extensions)

def load_and_preprocess_images(uploaded_file):
    images = []
    
    img = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    if img is not None:
        img = cv2.resize(img, (224, 224))
        img = np.stack((img,)*3, axis=-1)  # Convert grayscale to RGB
        images.append(img)

    return np.array(images)

def predict_image_outcome(images, model):
    if len(images) == 0:
        return {'decision': None, 'count_0': 0, 'count_1': 0}

    predictions = model.predict(images)
    predicted_labels = (predictions > 0.5).astype(int)  # Convert probabilities to binary labels

    # Count how many 0s and 1s
    count_0 = np.sum(predicted_labels == 0)
    count_1 = np.sum(predicted_labels == 1)

    decision = 1 if count_1 > count_0 else 0

    return {'decision': decision, 'count_0': count_0, 'count_1': count_1}

# Streamlit app
st.set_page_config(page_title="CT Scan Image Viewer", page_icon="🖼️", layout="wide", initial_sidebar_state="expanded")

# Custom HTML and CSS to set the video as the background
video_background_html = """
<style>
#root {
    overflow: visible;  /* Ensures that nothing is clipped and scrollbars are visible if needed */
}

#bgVideo {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100vw;  /* Ensures the video width matches the viewport width */
    height: 100vh;  /* Ensures the video height matches the viewport height */
    object-fit: cover;  /* Cover the area without losing aspect ratio */
    z-index: -1;  /* Ensures the video stays behind all other content */
}

.stApp {
    z-index: 1;  /* Ensures Streamlit content overlays the video */
    background: transparent;  /* Makes Streamlit background transparent to see the video behind */
}

.content {
    padding: 1rem;  /* Padding for content within the Streamlit app */
    color: #fff;  /* Color for content to ensure it is readable over the video */
}
</style>

<video id="bgVideo" autoplay loop muted playsinline>
    <source src="https://cdn.pixabay.com/video/2021/04/04/69951-538962240_large.mp4" type="video/mp4">
    Your browser does not support HTML5 video.
</video>
"""

st.markdown(video_background_html, unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("About")
    st.info("This application allows you to upload and view CT scan images. Your data privacy is respected and no data is stored.")
    st.header("Analysis Options")
    processing_option = st.selectbox("Choose analysis type:", ["Type 1", "Type 2", "Type 3"])
    st.text_area("Notes:", "Enter some notes here...")

# Main application content with title and file uploader
st.title('CT Scan Image Viewer')
uploaded_file = st.file_uploader("Upload your CT scan image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded CT Scan', use_column_width=True)
    
    # Load and preprocess the uploaded image
    images = load_and_preprocess_images(uploaded_file)
    
    # Load the pre-trained model
    model_path = "Desktop/Pretrained Model.h5"  # Update this path if necessary
    model = load_model(model_path)
    
    # Predict the outcome
    with st.spinner('Processing image...'):
        outcome = predict_image_outcome(images, model)
    
    # Display prediction results
    st.success("Image successfully processed!")
    st.write(f"Decision: {'Surgery Needed' if outcome['decision'] == 1 else 'No Surgery Needed'}")
    st.write(f"Count of Class 0: {outcome['count_0']}")
    st.write(f"Count of Class 1: {outcome['count_1']}")
else:
    st.info("Please upload an image to proceed.")
