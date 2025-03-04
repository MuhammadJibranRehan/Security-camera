import streamlit as st
import requests
import tempfile
import os

# Flask server URL
SERVER_URL = "https://security-camera.streamlit.app/"

st.title("🔒 Security Camera App")

# Show the video feed
st.image(f"{SERVER_URL}/video_feed")

# Start recording button
if st.button("Start Recording"):
    requests.post(f"{SERVER_URL}/start_record")
    st.success("Recording Started!")

# Stop recording button
if st.button("Stop Recording"):
    requests.post(f"{SERVER_URL}/stop_record")
    st.success("Recording Stopped!")

# Fetch and display the last recorded video
st.subheader("📹 Recorded Video")
if st.button("Get Last Recorded Video"):
    response = requests.get(f"{SERVER_URL}/get_last_video")
    if response.status_code == 200:
        temp_video_path = os.path.join(tempfile.gettempdir(), "last_video.avi")
        with open(temp_video_path, "wb") as f:
            f.write(response.content)
        st.video(temp_video_path)
    else:
        st.error("No recorded video found!")

# Upload video section
st.subheader("📤 Upload a Video")
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi"])

if uploaded_file is not None:
    files = {"video": uploaded_file.getvalue()}
    response = requests.post(f"{SERVER_URL}/upload", files=files)
    if response.status_code == 200:
        st.success("Video Uploaded Successfully!")
    else:
        st.error("Upload Failed")
