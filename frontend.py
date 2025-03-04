import streamlit as st
import requests
import cv2
import numpy as np
from PIL import Image
import os

SERVER_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Security Camera App", layout="centered")
st.markdown("<h1 style='text-align: center;'>🔒 Security Camera App</h1>", unsafe_allow_html=True)

# Display live camera feed
st.image(f"{SERVER_URL}/video_feed")

# Buttons for recording
col1, col2 = st.columns(2)
with col1:
    if st.button("Start Recording", use_container_width=True):
        response = requests.post(f"{SERVER_URL}/start_recording")
        st.success(response.json()["message"])

with col2:
    if st.button("Stop Recording", use_container_width=True):
        response = requests.post(f"{SERVER_URL}/stop_recording")
        st.success(response.json()["message"])

# File uploader for video
st.markdown("### Upload a video")
uploaded_file = st.file_uploader("Drag and drop file here", type=["mp4", "avi", "mpeg4"])

if uploaded_file:
    st.video(uploaded_file)

# Get last recorded video
if st.button("Get Last Recorded Video"):
    response = requests.get(f"{SERVER_URL}/latest_video")
    if response.status_code == 200:
        video_path = response.json()["latest_video"]
        st.video(video_path)
    else:
        st.warning("No recorded video found.")
