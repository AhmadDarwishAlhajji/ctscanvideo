import streamlit as st
from PIL import Image

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
uploaded_file = st.file_uploader("Upload your CT scan image", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded CT Scan', use_column_width=True)
    with st.spinner('Processing image...'):
        # Simulating a long processing task
        import time
        time.sleep(5)
    st.success("Image successfully processed!")
else:
    st.info("Please upload an image to proceed.")
