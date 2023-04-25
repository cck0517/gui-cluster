import streamlit as st
import cv2
import numpy as np

# Set page config
st.set_page_config(layout="wide")

# Define sidebar widgets
video_file = st.sidebar.file_uploader("Select video file", type=["mp4", "avi", "mov"])
play_button = st.sidebar.button("Play")
pause_button = st.sidebar.button("Pause")
frame_number = st.sidebar.number_input("Frame number", min_value=0, value=0)

# Create OpenCV video capture object
if video_file is not None:
    file_bytes = np.asarray(bytearray(video_file.read()), dtype=np.uint8)
    cap = cv2.VideoCapture()
    cap.open(video_file.name, cv2.CAP_FFMPEG)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
else:
    cap = None

# Set video position to current frame number
if cap is not None:
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

# Read current frame from video capture
if cap is not None:
    ret, frame = cap.read()
    if not ret:
        print("not ret!")
else:
    frame = np.zeros((720, 1280, 3), dtype=np.uint8)

# Resize frame to fit in Streamlit app
frame = cv2.resize(frame, (640, 360))

# Convert frame to RGB format
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Display frame in Streamlit app
video_container = st.empty()
video_container.image(frame, use_column_width=True)

# Handle Play button press
if play_button:
    while cap is not None:
        ret, frame = cap.read()
        if not ret:
            print("not ret!")
            break
        frame = cv2.resize(frame, (640, 360))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_container.image(frame, use_column_width=True)
        frame_number += 1
        st.sidebar.number_input("Frame number", min_value=0, value=frame_number)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        if not play_button:
            break
        st.experimental_rerun()

# Handle Pause button press
if pause_button:
    cap.release()

# Release video capture
if cap is not None:
    cap.release()