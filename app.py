import streamlit as st
import cv2
import numpy as np
import time

#from streamlit_state.session_state import SessionState
st.set_page_config(layout="wide")

# Create sidebar widgets
video_file = st.sidebar.file_uploader("Select video file", type=["mp4", "avi", "mov"])
play_button = st.sidebar.button("Play")
pause_button = st.sidebar.button("Pause")

# Set up OpenCV video capture
if video_file is not None:
    file_bytes = np.asarray(bytearray(video_file.read()), dtype=np.uint8)
    cap = cv2.VideoCapture()
    cap.open(video_file.name, cv2.CAP_FFMPEG)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
else:
    cap = None

# Initialize scroll bar value
bar = st.empty()
if cap is not None:
    scroll_pos = bar.slider("Frame", 0, frame_count - 1, 0)
else:
    scroll_pos = 0

# Set video position to current scroll bar value
if cap is not None:
    cap.set(cv2.CAP_PROP_POS_FRAMES, scroll_pos)

# Read current frame from video capture
if cap is not None:
    ret, frame = cap.read()
else:
    frame = np.zeros((720, 1280, 3), dtype=np.uint8)

# Resize frame to fit in Streamlit app
frame = cv2.resize(frame, (640, 360))

# Convert frame to RGB format
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Display frame in Streamlit app
video_container = st.empty()
video_container.image(frame, use_column_width=True)

# when play button is pressed, update the frames as well as the scroll bar value
if play_button:
    while cap is not None:
        scroll_pos += 1
        bar.slider("Frame", 0, frame_count - 1, scroll_pos)
        cap.set(cv2.CAP_PROP_POS_FRAMES, scroll_pos)
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (640, 360))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_container.image(frame, use_column_width=True)
        if pause_button:
            break


# Release video capture
if cap is not None:
    cap.release()
    

