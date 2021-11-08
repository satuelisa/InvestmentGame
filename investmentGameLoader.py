# http://ajaxload.info/ es lo que genera la ruedita de espera
from Tkinter import *
from PIL import Image, ImageTk

class Loader(Label):

    def __init__(self, root, img):
        src = Image.open(img)
        imageFrames =  list()
        try:
            while True:
                imageFrames.append(src.copy())
                src.seek(len(imageFrames))
        except EOFError:
            pass
        try:
            self.delay = src.info['duration']
        except KeyError:
            self.delay = 50
        first = imageFrames[0].convert('RGBA')
        self.frames = [ImageTk.PhotoImage(first)]
        Label.__init__(self, root, image = self.frames[0])
        temp = imageFrames[0]
        for f in imageFrames[1:]:
            temp.paste(f)
            frame = temp.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame))
        self.pos = 0
        self.rounds = 0
        self.waiter = None
        return

    def animate(self, r, w):
        self.rounds = r
        self.waiter = w
        self.after(0, self.step)

    def step(self):
        self.config(image = self.frames[self.pos])
        self.pos += 1
        if self.pos == len(self.frames):
            self.pos = 0
        if self.rounds > 0:
            self.rounds -= 1
            if self.rounds == 0:
                self.waiter.signal()
            else:
                self.after(self.delay, self.step)
        return
