import streamlit as st
import requests
import tempfile
import os

# 🚀 REPLACE with your deployed backend URL
SERVER_URL = "https://your-backend.onrender.com"

st.title("🔒 Security Camera App")

# Video Stream (Not implemented here)
st.image(f"{SERVER_URL}/video_feed")

# 🎥 Start Recording
if st.button("Start Recording"):
    response = requests.post(f"{SERVER_URL}/start_record")
    if response.status_code == 200:
        st.success("Recording Started!")
    else:
        st.error("Failed to start recording.")

# 🛑 Stop Recording
if st.button("Stop Recording"):
    response = requests.post(f"{SERVER_URL}/stop_record")
    if response.status_code == 200:
        st.success("Recording Stopped!")
    else:
        st.error("Failed to stop recording.")

# 📂 File Upload
uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mpeg4"])
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    with open(temp_file_path, "rb") as file:
        response = requests.post(f"{SERVER_URL}/upload", files={"file": file})

    os.remove(temp_file_path)  # Clean up temp file

    if response.status_code == 200:
        st.success("File uploaded successfully!")
    else:
        st.error("Failed to upload file.")

# 🎬 Display Last Recorded Video
if st.button("Get Last Recorded Video"):
    video_url = f"{SERVER_URL}/get_last_video"
    st.video(video_url)
