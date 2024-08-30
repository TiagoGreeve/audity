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

CHUNK = 1024

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