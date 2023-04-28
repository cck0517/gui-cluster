import streamlit as st
import cv2
import numpy as np

#create session state object pos
if 'pos' not in st.session_state:
    st.session_state.pos = 0

# Define the video player class

class Videoplayer():
    #define the initialization process

    def __init__(self,video_path):
        
        # create video capture 
        self.video_path = video_path
        self.cap = cv2.VideoCapture()
        self.opened=self.cap.open(video_path)
        if self.opened:
            print("initialized successfully")
        else:
            st.error("unable to initialize video")
        
        #set up the scroll bar with an st.slider
        self.pos = st.session_state.pos
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.bar = st.empty()
        self.pos = self.bar.slider("Frame",0,self.frame_count,self.pos)

        #display the first frame
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.pos)
        self.video_container = st.empty()
        ret,frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.video_container.image(frame)
        else:
            st.error("can not read frame")
        
        # set up the play button and pause button
        self.play_button = st.button("Play")
        self.pause_button = st.button("Pause")
        
        
        #set up boolean value is_playing
        self.is_playing = False
        
        if self.play_button:
            self.is_playing=True
            self.play()
    
    # play function
    def play(self):
        while self.is_playing:
            st.session_state.pos =  self.pos+1
            self.pos =  st.session_state.pos
            self.bar.slider("Frame",0,self.frame_count,self.pos)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.pos)
            ret,frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.video_container.image(frame)
            else:
                st.error(f'cannot read frame # {self.pos}')
            """ if self.pos>= self.frame_count:
                break """
            if self.pause_button:
                self.is_playing=False
                break
        self.pause(self.pos)
    
    #   pause function
    def pause(self,pos):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        ret,frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.video_container.image(frame)
        else:
            st.error(f'cannot read frame # {self.pos}')
    



        
    
    





















player = Videoplayer("C:\\Users\\16152\\Desktop\\sample.mp4")



        

