import tkinter as tk
import pygame
import cv2
import glob
import PIL.Image, PIL.ImageTk
import time
import math
import cv2
import cvzone
from ultralytics import YOLO
import os
path = os.path.dirname(os.path.realpath(__file__))
model = YOLO(path+"/best5.pt")
classNames = ['Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest', 'Person', 'Safety Cone', 'Safety Vest', '-', '-']
pygame.mixer.init()
pygame.mixer.music.load(path+"/alert.mp3")

class Alert:
    def __init__(self):
        self.sudah_diakses


class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.frame0 = tk.Frame(self.window)
        self.frame0.pack(expand=True,fill="both")
        self.frame1 = tk.Frame(self.frame0,background="#303030")
        self.frame1.pack(side="left",expand=True,fill="both")
        self.frame2 = tk.Frame(self.frame0,background="#303030")
        self.frame2.pack(side="left",expand=True,fill="both")
        self.window.title(window_title)
        self.window["bg"] = "#303030"
        self.video_source = video_source
        self.loop = 0

        # membuka sumber video (secara default akan mengambil webcam sebagai sumber video)
        self.vid = MyVideoCapture(self.video_source)

        # setting window menjadi fullscreen
        window.attributes("-fullscreen", True)
        window.bind("<Escape>", self.exit_fullscreen)
        
        
        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(self.frame1, width = self.vid.width, height = self.vid.height)
        self.canvas.pack(pady=20)
        self.canvas2 = tk.Canvas(self.frame2, width = self.vid.width, height = self.vid.height)
        self.canvas2.pack(pady=20)

        self.label = tk.Label(text="")
        self.label.pack(pady=50)

        # tombol untuk menghentikan alert yang berbunti
        self.btn_stopAlert=tk.Button(window, text="Stop Alert", width=50, command=self.stopAlert,activebackground='red',activeforeground='yellow')
        self.btn_stopAlert.pack(anchor=tk.CENTER, expand=True)

        # Setelah dipanggil satu kali, fungsi update akan dipanggil kembali setiap 10 milidetik
        self.delay = 10
        self.update()

        self.window.mainloop()
    def exit_fullscreen(self,event):
        self.window.attributes("-fullscreen", False)


    def alert(self,text,frame):
        if text != "":
            cv2.imwrite(path + "/img/frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            list_of_files = glob.glob(path+'/img/*.jpg')
            latest_file = max(list_of_files, key=os.path.getctime)
            self.img = PIL.ImageTk.PhotoImage(PIL.Image.open(latest_file))
            self.canvas2.create_image(0, 0, image = self.img, anchor = tk.NW)
            pygame.mixer.music.play(loops=self.loop)

    def stopAlert(self):

        Alert.sudah_diakses=False
        pygame.mixer.music.stop()

    def update(self):

        # mengambil setiap frame pada video
        success, frame, currentAlert = self.vid.get_frame()

        if success:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
            if not hasattr(Alert,"sudah_diakses") or not Alert.sudah_diakses:
                self.loop = -1
                self.alert(currentAlert,frame)
                if currentAlert != "":
                    Alert.sudah_diakses = True

            self.label.configure(text=currentAlert)
        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # membuka sumber video
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Tidak dapat membuka sumber video", video_source)
        
        # mengambil lebar dan tinggi dari sumber video
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            success, frame = self.vid.read()
            results = model(frame, stream=True)
            alert=''
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    # Bounding Box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    # Confidence
                    conf = math.ceil((box.conf[0] * 100))
                    # Class Name
                    cls = int(box.cls[0])
                    currentClass = classNames[cls]
                    if conf > 50:
                        if currentClass =='NO-Hardhat' or currentClass =='NO-Safety Vest' or currentClass == "NO-Mask":
                            alert  += currentClass
                            myColor = (0, 0,255)
                        elif currentClass =='Hardhat' or currentClass =='Safety Vest' or currentClass == "Mask":
                            myColor =(0,255,0)
                        else:
                            myColor = (255, 0, 0)

                        cvzone.putTextRect(frame, f'{classNames[cls]} {conf}',
                                        (max(0, x1), max(35, y1)), scale=1, thickness=0,colorB=myColor,
                                        colorT=(255,255,255),colorR=myColor, offset=5)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), myColor, 1)
            # mengembalikan nilai boolean berupa success, setiap frame yang telah diubah ke format RGB, dan teks class yang akan memicu alert 
            return (success, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),alert)
        else:
            return (success, None)

    # melepaskan source video ketika aplikasi ditutup
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# membuat window aplikasi menggunakan tkinter
# App(tk.Tk(), "APLIKASI DETEKSI KELALAIAN ALAT PELINDUNG DIRI (APD)",video_source= path +"/Videos/ppe-1.mp4")
App(tk.Tk(), "APLIKASI DETEKSI KELALAIAN ALAT PELINDUNG DIRI (APD)",video_source=1)