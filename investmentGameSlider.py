from Tkinter import *

HEIGHT = 60
CANAL = 10
MARKER = 10

class InvestmentGameSlider(Frame):

    def setup(self, max, lc, rc, width, ticks = False, value = True): 
        global MARKER, CANAL
        self.max = max
        self.slider.configure(length = width)
        self.slider.configure(width = CANAL)
        self.slider.configure(sliderlength = MARKER)
        self.slider.configure(sliderrelief = FLAT)
        self.slider.configure(troughcolor = 'black')
        if not value:
            self.slider.configure(showvalue = 0)
        # self.slider.configure(orient = VERTICAL)
        self.slider.configure(relief = FLAT)
        self.slider.configure(to = self.max)
        self.slider.configure(tickinterval = 0)
        
        self.leftColor = lc
        self.rightColor = rc
        self.update()
        # print 'Indicator bar maximum set to %d.' % self.max
        return

    def grid(self, row = None, column = None, \
                 columnspan = None, rowspan = None, padx = None, ipady = None, sticky = None):
        if sticky is None:
            sticky = W
        Frame.grid(self, row = row, column = column, \
                       columnspan = columnspan, rowspan = rowspan, ipady = ipady, sticky = sticky)
        self.slider.grid(row = row, column = column, \
                             columnspan = columnspan - 1, rowspan = 1, \
                             padx = padx, sticky = N + sticky)
        self.bar.grid(row = row + 1, column = column, \
                          columnspan = columnspan - 1, rowspan = rowspan - 1, \
                          padx = padx, sticky = N + sticky)
        self.label.grid(row = row + 1, column = column + columnspan - 1, rowspan = 1, columnspan = 1, \
                            padx = padx, sticky = S + sticky)
        return

    def __init__(self, target, amount):
        Frame.__init__(self, target)
        self.bar = Canvas(self)
        self.configure(bd = 0, highlightthickness = 0)
        self.bar.configure(bd = 0, highlightthickness = 0)
        self.leftColor = None
        self.rightColor = None
        self.left = None
        self.right = None
        self.max = None
        if amount is None:
            self.label = Label(self, text = '', font = ('Helvetica', 24))
        else:
            self.label = Label(self, text = amount, font = ('Helvetica', 24))
        self.slider = Scale(target, from_ = 0, \
                                to = 100, \
                                orient = HORIZONTAL, \
                                tickinterval = 10, \
                                font = ('Helvetica', 18))
        return
        
    def bind(self, button, method):
        self.slider.bind(button, method)
        return

    def scale(self):
        return self.slider

    def update(self):
        global HEIGHT
        if self.max is not None:
            # print 'Updating the indicator bar.'
            w = self.slider.cget('length')
            h = HEIGHT

            self.bar.configure(width = w, height = HEIGHT)

            w = int(self.bar.cget('width'))
            h = int(self.bar.cget('height'))

            if self.max > 0.0:
                x = int(round((self.slider.get() * 1.0 / self.max) * w))
            else:
                x = w

            if self.left is not None:
                self.bar.delete(self.left)
            if x > 0:
                self.left = \
                    self.bar.create_rectangle(0, 0, x, h, \
                                                  fill = self.leftColor, width = 0)
            if self.right is not None:
                self.bar.delete(self.right)
            if x < w:
                self.right = \
                    self.bar.create_rectangle(x, 0, w, h, \
                                                  fill = self.rightColor, width = 0)
        return

    def set(self, value):
        self.slider.set(value)
        self.update()
        return

    def background(self, color):
        self.label.configure(bg = color)
        self.slider.configure(bg = color)
        self.bar.configure(bg = color)
        self.configure(bg = color)
        return
        
    def disable(self):
        self.slider.configure(state = DISABLED)

    def enable(self):
        self.slider.configure(state = NORMAL)

    def get(self):
        return self.slider.get()


