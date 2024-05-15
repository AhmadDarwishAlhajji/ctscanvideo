import streamlit as st
from PIL import Image
import numpy as np
import cv2
from tensorflow.keras.models import load_model

# Load your model
model = load_model('Desktop/Pretrained Model.h5')  # Update this path if needed

# Setting the page configuration to use the full page width and a custom title
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
uploaded_file = st.file_uploader("Upload your CT scan image", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_file:
    predictions = []
    for file in uploaded_file:
        image = Image.open(file).convert('L')  # Convert to grayscale
        img_array = np.array(image)
        img_resized = cv2.resize(img_array, (128, 128)) / 255.0
        img_resized = img_resized.reshape(-1, 128, 128, 1)
        prediction = model.predict(img_resized)
        predictions.append(int(prediction[0][0] > 0.5))
        st.image(image, caption=f'Uploaded CT Scan {file.name}', use_column_width=True)

    with st.spinner('Processing images...'):
        import time
        time.sleep(5)
    
    surgery_needed = sum(predictions) >= 10
    st.success(f"Prediction complete! {'Surgery is needed' if surgery_needed else 'Surgery is not needed'}")
else:
    st.info("Please upload images to proceed.")
