import math

import cvzone
import av
import cv2
import numpy as np
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
from ultralytics import YOLO

model = YOLO("best5.pt")
classNames = ['Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest', 'Person', 'Safety Cone', 'Safety Vest']
myColor = (0, 0, 255)

def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    image = frame.to_ndarray(format="bgr24")
    results = model(image, stream=True)
    for r in results:
            boxes = r.boxes
            for box in boxes:
                # Bounding Box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Confidence
                conf = math.ceil((box.conf[0] * 100)) / 100
                # Class Name
                cls = int(box.cls[0])
                currentClass = classNames[cls]
                if conf>0.5:
                    if currentClass =='NO-Hardhat' or currentClass =='NO-Safety Vest' or currentClass == "NO-Mask":
                        myColor = (0, 0,255)
                    elif currentClass =='Hardhat' or currentClass =='Safety Vest' or currentClass == "Mask":
                        myColor =(0,255,0)
                    else:
                        myColor = (255, 0, 0)

                    cvzone.putTextRect(image, f'{classNames[cls]} {conf}',
                                    (max(0, x1), max(35, y1)), scale=1, thickness=2,colorB=myColor,
                                    colorT=(255,255,255),colorR=myColor, offset=5)
                    cv2.rectangle(image, (x1, y1), (x2, y2), myColor, 3)
    return av.VideoFrame.from_ndarray(image, format="bgr24")
    
st.title('APLIKASI DETEKSI KELALAIAN ALAT PELINDUNG DIRI (APD) PADA PEKERJA KONSTRUKSI')


webrtc_ctx = webrtc_streamer(
    key="sample",
    mode=WebRtcMode.SENDRECV,
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
    async_processing=True,
)
