import os
import tkinter as Tkinter
from pynput import keyboard
from tkinter import END

class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

    def hasPrev(self):
        return self.prev is not None

    def hasNext(self):
        return self.next is not None

    def getPrev(self):
        return self.prev

    def getNext(self):
        return self.next

    def setPrev(self, node):
        self.prev = node

    def setNext(self, node):
        self.next = node

    def __str__(self):
        return str(self.hasPrev()) + ", " + str(self.hasNext())


class Song:
    def __init__(self, name, artist=None, features=None, album=None):
        self.name = name
        self.artist = artist
        self.features = features
        self.album = album

    def __str__(self):
        return str(self.name) + " by " + str(self.artist) + " Ft. " + str(self.features)


class Album:
    def __init__(self, name, songs=None):
        self.name = name
        self.songs = songs

    def __str__(self):
        return str(self.name) + ": " + str(self.songs)




def get_files_with_ext(path, extensions):
    res = []
    for file in os.listdir(path):
        if file.split('.')[-1] in extensions:
            res.append(file)

    return res

def filter_with_ext(files, extensions):
    res = []
    for file in files:
        if file.split('.')[-1] in extensions:
            res.append(file)

    return res


class DragDropListbox(Tkinter.Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """
    def __init__(self, master, collection, **kw):
        kw['selectmode'] = Tkinter.SINGLE
        self.collection = collection
        Tkinter.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.setCurrent)
        # self.bind('<ButtonRelease-1>', self.deselect)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None

    # def insert(self, index, *elements):
    #

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    # def deselect(self, event):
    #     self.selection_clear(0, END)

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            c = self.collection.pop(i)
            self.delete(i)
            self.insert(i+1, x)
            self.collection.insert(i+1, c)
            self.curIndex = i
            print(self.collection[0])
        elif i > self.curIndex:
            x = self.get(i)
            c = self.collection.pop(i)
            self.delete(i)
            self.insert(i-1, x)
            self.collection.insert(i - 1, c)
            self.curIndex = i
            print(self.collection[0])


# class ReorderableListbox(tk.Listbox):
#     """ A Tkinter listbox with drag & drop reordering of lines """
#     def __init__(self, master, **kw):
#         kw['selectmode'] = tk.EXTENDED
#         tk.Listbox.__init__(self, master, kw)
#         self.bind('<Button-1>', self.setCurrent)
#         self.bind('<Control-1>', self.toggleSelection)
#         self.bind('<B1-Motion>', self.shiftSelection)
#         self.bind('<Leave>',  self.onLeave)
#         self.bind('<Enter>',  self.onEnter)
#         self.selectionClicked = False
#         self.left = False
#         self.unlockShifting()
#         self.ctrlClicked = False
#     def orderChangedEventHandler(self):
#         pass
#
#     def onLeave(self, event):
#         # prevents changing selection when dragging
#         # already selected items beyond the edge of the listbox
#         if self.selectionClicked:
#             self.left = True
#             return 'break'
#     def onEnter(self, event):
#         #TODO
#         self.left = False
#
#     def setCurrent(self, event):
#         self.ctrlClicked = False
#         i = self.nearest(event.y)
#         self.selectionClicked = self.selection_includes(i)
#         if (self.selectionClicked):
#             return 'break'
#
#     def toggleSelection(self, event):
#         self.ctrlClicked = True
#
#     def moveElement(self, source, target):
#         if not self.ctrlClicked:
#             element = self.get(source)
#             self.delete(source)
#             self.insert(target, element)
#
#     def unlockShifting(self):
#         self.shifting = False
#     def lockShifting(self):
#         # prevent moving processes from disturbing each other
#         # and prevent scrolling too fast
#         # when dragged to the top/bottom of visible area
#         self.shifting = True
#
#     def shiftSelection(self, event):
#         if self.ctrlClicked:
#             return
#         selection = self.curselection()
#         if not self.selectionClicked or len(selection) == 0:
#             return
#
#         selectionRange = range(min(selection), max(selection))
#         currentIndex = self.nearest(event.y)
#
#         if self.shifting:
#             return 'break'
#
#         lineHeight = 15
#         bottomY = self.winfo_height()
#         if event.y >= bottomY - lineHeight:
#             self.lockShifting()
#             self.see(self.nearest(bottomY - lineHeight) + 1)
#             self.master.after(500, self.unlockShifting)
#         if event.y <= lineHeight:
#             self.lockShifting()
#             self.see(self.nearest(lineHeight) - 1)
#             self.master.after(500, self.unlockShifting)
#
#         if currentIndex < min(selection):
#             self.lockShifting()
#             notInSelectionIndex = 0
#             for i in selectionRange[::-1]:
#                 if not self.selection_includes(i):
#                     self.moveElement(i, max(selection)-notInSelectionIndex)
#                     notInSelectionIndex += 1
#             currentIndex = min(selection)-1
#             self.moveElement(currentIndex, currentIndex + len(selection))
#             self.orderChangedEventHandler()
#         elif currentIndex > max(selection):
#             self.lockShifting()
#             notInSelectionIndex = 0
#             for i in selectionRange:
#                 if not self.selection_includes(i):
#                     self.moveElement(i, min(selection)+notInSelectionIndex)
#                     notInSelectionIndex += 1
#             currentIndex = max(selection)+1
#             self.moveElement(currentIndex, currentIndex - len(selection))
#             self.orderChangedEventHandler()
#         self.unlockShifting()
#         return 'break'
