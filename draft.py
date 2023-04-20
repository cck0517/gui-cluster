import streamlit as st
import cv2
import numpy as np
import time

class VideoPlayer:
    def __init__(self):
        self.cap = None
        self.frame_count = None
        self.fps = None
        self.scroll_pos = 0
        self.is_playing = False
    
    def load_video(self, video_file):
        file_bytes = np.asarray(bytearray(video_file.read()), dtype=np.uint8)
        self.cap = cv2.VideoCapture()
        self.cap.open(video_file.name, cv2.CAP_FFMPEG)
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    
    def update_frame(self,pos,frame_given=None,key=None):
        if self.cap is not None:
            if frame_given is not None:
                 frame = frame_given
                 frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                 self.cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
                 ret, frame = self.cap.read()
                 if not ret:
                     return
            frame = cv2.resize(frame, (640, 360))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.video_container.image(frame, use_column_width=True)
            if key is not None:
                self.scroll_pos = self.scroll_bar.slider("Frame", 0, player.frame_count - 1, player.scroll_pos,key = key)
            else:
                self.scroll_pos = self.scroll_bar.slider("Frame", 0, player.frame_count - 1, player.scroll_pos)
            #self.scroll_pos += 1
            #self.scroll_pos = self.scroll_pos % self.frame_count
            #time.sleep(1/self.fps)
    
    def run(self):
        
        ## set up lay out
        st.set_page_config(layout="wide")
        
        # set up different widgets
        self.video_file = st.sidebar.file_uploader("Select video file", type=["mp4", "avi", "mov"])
        self.play_button = st.sidebar.button("Play",on_click=self.play)
        self.pause_button = st.sidebar.button("Pause")
        
        # set up containers
        self.video_container = st.empty()
        self.scroll_bar = st.sidebar.empty()
        
        # load the video
        if self.video_file is not None:
                self.load_video(self.video_file)
        
        if player.cap is not None:
            player.scroll_pos = player.scroll_bar.slider("Frame", 0, player.frame_count - 1, player.scroll_pos)

        if player.cap is not None:
            player.cap.set(cv2.CAP_PROP_POS_FRAMES, player.scroll_pos)

        if player.cap is not None:
            ret, frame = player.cap.read()
        else:
            frame = np.zeros((720, 1280, 3), dtype=np.uint8)

        frame = cv2.resize(frame, (640, 360))

# Convert frame to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Display frame in Streamlit app
        player.update_frame(player.scroll_pos,frame)

    def play(self):
        player.is_playing=True
        while player.is_playing:
            if player.pause_button:
                  player.is_playing=False
            self.scroll_pos+=1
            self.update_frame(player.scroll_pos)
        self.update_frame(player.scroll_pos,"pause")
    
    
        


                 
                 
         

            

    
            

player = VideoPlayer()
player.run()


             
