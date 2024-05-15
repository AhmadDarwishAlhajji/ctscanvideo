import streamlit as st
from PIL import Image
import numpy as np
import cv2
import time  # Added import for time module
from tensorflow.keras.models import load_model

try:
    import cv2  # Removed redundant import check
except ImportError as e:
    st.error(f"Failed to import cv2: {e}")

# Load the model
model_path = 'Desktop/Pretrained Model.h5'  # Update the path as necessary
try:
    model = load_model(model_path)
except Exception as e:
    st.error(f"Failed to load model: {e}")

# Setting the page configuration
st.set_page_config(page_title="CT Scan Image Viewer", page_icon="🖼️", layout="wide", initial_sidebar_state="expanded")

# Custom HTML and CSS for the video background (unchanged)...

# Sidebar configuration (unchanged)...

# Main application content with title and file uploader
st.title('CT Scan Image Viewer')
uploaded_file = st.file_uploader("Upload your CT scan image", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded CT Scan', use_column_width=True)
    with st.spinner('Processing image...'):
        # Image conversion and prediction
        img = cv2.imdecode(np.frombuffer(uploaded_file.getvalue(), np.uint8), cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (128, 128)) / 255.0
        img = img.reshape(-1, 128, 128, 1)
        prediction = model.predict(img)
        prediction_result = 'Surgery Needed' if prediction[0][0] > 0.5 else 'No Surgery Needed'
        time.sleep(5)  # Simulate processing time
    st.success(f"Image successfully processed! Result: {prediction_result}")
else:
    st.info("Please upload an image to proceed.")
