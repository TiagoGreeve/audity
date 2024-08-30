import tkinter as tk
from tkinter import ttk
  
import pyaudio
import wave
import sys
import subprocess
import os

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import INSERT
from tkinter import END
from tkinter import LEFT, RIGHT, BOTTOM
import threading

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

from utils import *


import collections
# from queue import LifoQueue
from pynput import keyboard

import sys


var = 0
queue = []
scalePressed = False
stack = []
time = 0

def on_press(key):
    global var
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['media_next']:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        print('skipping song')
        var = 2
    # if k in ['4']:
    #     print('Ending programme')
    #     var = 3
    # if k in ['5']:
    #     print('rewind by 10')
    #     var = 4
    # if k in ['6']:
    #     print('skip by 10')
    #     var = 5
    if k in ['media_previous']:
        print('starting again')
        var = 7
    if k in ['media_play_pause']:
        var = 8
    # if k in ['6']:
    #     print('rewind by 10')
    #     var = 5

path = r'C:\Users\tiago\play_audio\songs'
extensions = ['mp3', 'wav']
fileList = get_files_with_ext(path, extensions)

iter = os.walk("C:\\Users\\tiago\\play_audio\\songs")
# for root, dirs, files in iter:
#     print(dirs)
#     break
next(iter)
albums = []
for root, dirs, files in iter:
    # print(root)
    if os.path.samefile(os.path.dirname(root), path):
        # print(root)
        albums.append(Album(os.path.basename(root), filter_with_ext(files, extensions)))

# for album in albums:
#     print(album)

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread
# listener.join()  # remove if main thread is polling self.keys






CHUNK = 1024



# if len(sys.argv) < 2:
#     print("Plays an audio file.\n\nUsage: %s filename.wav" % sys.argv[0])
#     sys.exit(-1)
#sys.argv[1]
# song = subprocess.Popen(["C:\\Users\\tiago\\Downloads\\ffmpeg-5.0.1-full_build\\bin\\ffmpeg.exe", "-i", sys.argv[1], "-loglevel", "panic", "-vn", "-f", "s16le", "pipe:1"],
#                         stdout=subprocess.PIPE, shell=True)

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=pyaudio.paInt16,
                channels=2,         # use ffprobe to get this from the file beforehand
                rate=44100,         # use ffprobe to get this from the file beforehand
                output=True)

# read data
# data = song.stdout.read(CHUNK)
# # print(var)
# # play stream (3)
# while len(data) > 0:
#     #print(var)
#     # print(var)
#     if (var < 1):
#         stream.write(data)
#         data = song.stdout.read(CHUNK)
#     if (var == 2):
#         song.kill()
#         break

#test
# song = subprocess.Popen(
#         ["C:\\Users\\tiago\\Downloads\\ffmpeg-5.0.1-full_build\\bin\\ffmpeg.exe", "-i", sys.argv[1], "-loglevel",
#          "panic", "-vn", "-f", "s16le", "pipe:1"],
#         stdout=subprocess.PIPE, shell=True)

# stack = LifoQueue()
# stack = collections.deque([])
# data = song.stdout.read(CHUNK)
# while len(data) > 0:
#     stack.append(data)
#     # stream.write(stack.get())
#     # stream.write(data)
#     data = song.stdout.read(CHUNK)
#
# print("hoi")
# print("SIKTER GIT\n")
# while len(stack) > 0:
#
#     stream.write(stack.popleft())

#endtest
# queue = []
# scalePressed = False

def pause():
    global var
    var = 1

def rewind():
    global var
    var = 4

def forward():
    global var
    var = 5

def prev():
    global var
    var = 7

def next_song():
    global var
    var = 2

global playlist
global now_playing
global scale

def main_loop():
    global playlist
    global now_playing
    global scale
    global var
    global queue
    while True:
        # name = ''
        if len(queue) == 0:
            continue
        else:
            name = queue.pop(0)
            playlist.delete(0)
        print('Now playing: ' + name)
        now_playing.config(text=name)
        var = 0
        song = subprocess.Popen(
            ["C:\\Users\\tiago\\Downloads\\ffmpeg-5.0.1-full_build\\bin\\ffmpeg.exe", "-i", "C:\\Users\\tiago\\play_audio\\songs\\" + name, "-loglevel",
            "panic", "-vn", "-f", "s16le", "pipe:1"],
            stdout=subprocess.PIPE, shell=True)

        data = song.stdout.read(CHUNK)
        curr = Node(data)
        tmp = curr
        data = song.stdout.read(CHUNK)
        num = 1
        paused = False
        while len(data) > 0:
            num = num + 1
            tmp.setNext(Node(data))
            tmp.getNext().setPrev(tmp)
            tmp = tmp.getNext()
            data  = song.stdout.read(CHUNK)
        # print(var)
        # play stream (3)
        scale.set(0)
        currNum = 0
        while curr.hasNext():
            if scalePressed is False:
                ratio = currNum / num
                now = ratio * 200
                scale.set(now)
            if (var < 1) and not paused:
                stream.write(curr.value)
                curr = curr.getNext()
                currNum = currNum + 1
            if (var == 1):
                paused = not paused
                var = 0
            if (var == 2):
                if len(queue) > 0:
                    song.kill()
                    break
                else:
                    var = 0
            if (var == 3):
                song.kill()
                break
            if (var == 4):
                cnt = 0
                while cnt < 1700 and curr.hasPrev():
                    curr = curr.getPrev()
                    currNum = currNum - 1
                    cnt = cnt + 1
                var = 0
            if (var == 5):
                cnt = 0
                while cnt < 1700 and curr.hasNext():
                    curr = curr.getNext()
                    currNum = currNum + 1
                    cnt = cnt + 1
                var = 0
            if var == 6:
                perunage = time / 200
                amount = perunage * num
                while curr.hasPrev():
                    curr = curr.getPrev()
                cnt = 0
                currNum = 0
                while cnt < amount and curr.hasNext():
                    curr = curr.getNext()
                    currNum = currNum + 1
                    cnt = cnt + 1
                var = 0
            if var == 7:
                if currNum < 850 and len(stack) > 0:
                    queue.insert(0, name)
                    temp = stack.pop()
                    queue.insert(0, temp)
                    song.kill()
                    playlist.insert(0, name + '\n')
                    playlist.insert(0, temp + '\n')
                    break
                else:
                    while curr.hasPrev():
                        curr = curr.getPrev()
                    currNum = 0
                    var = 0
            if var == 8:
                paused = not paused
                var = 0
            if var == 9:
                paused = False
        if var != 7:
            stack.append(name)
        scale.set(0)
        if var == 3:
            break

LARGEFONT =("Verdana", 35)
  
class tkinterApp(tk.Tk):
     
    # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        self.iconbitmap(r"C:\Users\tiago\PycharmProjects\pythonProject1\logo.ico")
        self.title('Audio player')
        # what does "" do?
        self.geometry("")
        window_width = 1000
        window_height = 600

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        # self.state('zoomed')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # creating a container
        container = ttk.Frame(self)  
        container.grid(sticky="nsew") 

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {}  
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(StartPage)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
  
# first window frame startpage
  
class StartPage(ttk.Frame):
    def __init__(self, parent, controller): 
        ttk.Frame.__init__(self, parent)

        global queue
        global var
        global playlist
        global now_playing
        global scale
        # r = tk.Tk()
        # self.iconbitmap(r"C:\Users\tiago\PycharmProjects\pythonProject1\logo.ico")
        # self.title('Audio player')
        # self.geometry("")
        # self.state('zoomed')
        
        # r.grid_columnconfigure(0, weight=1)
        # r.grid_columnconfigure(1, weight=1)
        # self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        style = ttk.Style()
        style.configure("RR.TFrame", foreground="black", background="red")
        mainframe = ttk.Frame(self)
        mainframe.grid(column=0, row=0, columnspan=4, rowspan=6, sticky="nsew")
        mainframe.grid_rowconfigure(0, weight=1)
        mainframe.grid_rowconfigure(1, weight=1)
        mainframe.grid_rowconfigure(2, weight=1)
        mainframe.grid_rowconfigure(3, weight=1)
        mainframe.grid_rowconfigure(4, weight=1)
        mainframe.grid_rowconfigure(5, weight=3)
        mainframe.grid_columnconfigure(0, weight=1)
        mainframe.grid_columnconfigure(1, weight=1)
        mainframe.grid_columnconfigure(2, weight=1)
        mainframe.grid_columnconfigure(3, weight=1)
        
        # Create a photoimage object of the image in the path
        # image1 = Image.open("C:/Users/tiago/Akin_as_art_final.png")
        # test = ImageTk.PhotoImage(image1)
        # label1 = tk.Label(image=test)
        # label1.image = test
        # label1.pack()
        # Position image

        buttons = ttk.Frame(mainframe)
        button = ttk.Button(buttons, text='pause/play', width=10, command=pause)

        buttonRewind = ttk.Button(buttons, text='rewind 10', width=10, command=rewind)

        buttonForward = ttk.Button(buttons, text='forward 10', width=10, command=forward)

        buttonPrev = ttk.Button(buttons, text="prev", width=10, command=prev)

        buttonNext = ttk.Button(buttons, text="next", width=10, command=next_song)

        buttonPrev.grid(column=1, row=0)
        buttonRewind.grid(column=2, row=0)
        button.grid(column=3, row=0)
        buttonForward.grid(column=4, row=0)
        buttonNext.grid(column=5, row=0)

        # entry = tk.Entry(mainframe, width=25)
        # entry.pack()
        # Songs
        style = ttk.Style()
        style.configure("BW.TFrame", foreground="black", background="white")
        song_frame = ttk.Frame(mainframe, style="BW.TFrame", height=10)
        album_frame = ttk.Frame(mainframe, style="BW.TFrame", height=10)
        song_frame.grid(column=0, row=0, columnspan=2, sticky="nsew", padx=5)
        album_frame.grid(column=2, row=0, columnspan=2, sticky="nsew", padx=5)
        song_frame.grid_rowconfigure(0, weight=1)
        song_frame.grid_columnconfigure(0, weight=1)
        album_frame.grid_rowconfigure(0, weight=1)
        album_frame.grid_columnconfigure(2, weight=1)
        #width=100, activestyle='none'
        songList = ttk.Treeview(song_frame, height=25, show="tree")
        for f in fileList:
            songList.insert("", END, text=f)
        songList.grid(column=0, row=0, columnspan=2, sticky="nsew")


        # scale = tk.Scale(mainframe, width=25, from_=0,to_=100, command=slide)
        # scale.pack()
        playlist = DragDropListbox(mainframe, queue, height=30, width=100, activestyle='none')
        def enter():
            for index in songList.selection():
                id = index[1:]
                id = int(id, 16) - 1
                playlist.insert(END, fileList[id] + '\n')
                # if queue is None:
                #     queue = Node(fileList[index])
                # else:
                #     queue.setNext(Node(fileList[index]))
                #     queue.getNext().setPrev(queue)
                queue.append(fileList[id])

        buttonEnterSongs = ttk.Button(song_frame, text='enter', width=25, command=enter)
        buttonEnterSongs.grid(column=0, row=1, columnspan=2)

        # albumList = tk.Listbox(mainframe, width=100)
        albumList = ttk.Treeview(album_frame, height=25, show="tree")
        for album in albums:
            albumList.insert("", END, text=album.name)
        albumList.grid(column=2, row=0, columnspan=2, sticky="nsew")
        def go(event):
            print("hey")

        def move(event):
            print("holla")

        # albumList.bind("<ButtonRelease-1>", go)
        # albumList.bind("<ButtonPress-1>", go)
        # albumList.bind("<B1-Motion>", move)

        # albumList.pack()
        #
        # bro = ReorderableListbox(tk.Listbox(mainframe, width=100))
        # bro.pack()

        def enter2():
            global queue
            for index in albumList.selection():
                index = index[1:]
                index = int(index, 16) - 1
                for song in albums[index].songs:
                    playlist.insert(END, song + '\n')
                    queue.append(albums[index].name + '\\' + song)
                # queue.extend(albums[index].songs)
        buttonEnter2 = ttk.Button(album_frame, text='enter', width=25, command=enter2)
        buttonEnter2.grid(column=2, row=1, columnspan=2)

    # height = 1
        now_playing = ttk.Label(mainframe, text='', width=40, anchor="w")
        now_playing.grid(column=1, row=2, columnspan=2)
        # , showvalue=0, activebackground='red'
        scale = ttk.Scale(mainframe, length=100, from_=0, to=200, orient='horizontal')
        def slide(event):
            global var
            global time
            global scalePressed
            var = 6
            time = scale.get()
            scalePressed = False
        def pressed(event):
            global scalePressed
            scalePressed = True
        scale.bind("<ButtonRelease-1>", slide)
        scale.bind("<ButtonPress-1>", pressed)
        buttons.grid(column=0, row=3, columnspan=4)
        scale.grid(column=1, row=4, columnspan=2)

        playlist.grid(column=1, row=5, columnspan=2, sticky="nsew")

        




  
        button1 = ttk.Button(buttons, text ="Page 1",
        command = lambda : controller.show_frame(Page1))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 0, column = 0, padx = 5)
  
        ## button to show frame 2 with text layout2
        button2 = ttk.Button(buttons, text ="Page 2",
        command = lambda : controller.show_frame(Page2))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 0, column = 6, padx = 5)
  
          
  
  
# second window frame page1 
class Page1(ttk.Frame):
     
    def __init__(self, parent, controller):
         
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Page 1", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="StartPage",
                            command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place 
        # by using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text ="Page 2",
                            command = lambda : controller.show_frame(Page2))
     
        # putting the button in its place by 
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
  
  
  
  
# third window frame page2
class Page2(ttk.Frame): 
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Page 2", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="Page 1",
                            command = lambda : controller.show_frame(Page1))
     
        # putting the button in its place by 
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text ="Startpage",
                            command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
  
  
# Driver Code
        


t1 = threading.Thread(target=main_loop)
t1.start() 
app = tkinterApp()
app.mainloop()