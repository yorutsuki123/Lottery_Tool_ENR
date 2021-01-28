import tkinter as tk
from PIL import Image, ImageTk
from itertools import count

def emptyFunc():
    pass

class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im, x, y, s=26, e=52, endDo=emptyFunc):
        self.endDo = endDo
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy().resize((x, y), Image.ANTIALIAS)))
                im.seek(i)
        except EOFError:
            pass
        self.frames = self.frames[s:e]
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            if self.loc < len(self.frames):
                self.config(image=self.frames[self.loc])
                self.after(self.delay, self.next_frame)
            else:
                self.endDo()
                self.unload()