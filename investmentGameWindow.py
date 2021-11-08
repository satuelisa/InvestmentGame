from Tkinter import *
from PIL import Image, ImageTk
from time import time
from random import randint
from math import fabs, floor
import investmentGameLoader as ldr
import investmentGameSlider as sld

class InvestmentGameFullScreen(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.protocol('WM_DELETE_WINDOW', self.close)
        padding = 5
        self.alternative = '600x400+0+0'
        w = self.winfo_screenwidth() - padding
        h = self.winfo_screenheight() - padding
        self.geometry('{0}x{1}+0+0'.format(w, h))
        self.bind('<Escape>', self.switchShape)
        return

    def enableEditing(self):
        self.button.configure(state = NORMAL)
        self.slider.enable()
        self.slider.set(0)
        if self.parameters['message']:
            self.comments.configure(state = NORMAL)
            self.comments.delete(1.0, END) # remove all previous text
        return

    def disableAll(self):
        self.button.configure(state = DISABLED)
        self.slider.disable()
        if self.parameters['message']:
            self.comments.delete(1.0, END) # remove all previous text
            self.comments.configure(state = DISABLED)
        return

    def switchShape(self, event):
        actual = self.winfo_geometry()
        self.geometry(self.alterative)
        self.alternative = actual
        return

    def close(self):
        self.destroy()
        return

class InvestmentGameWindow(InvestmentGameFullScreen):

    def resource(self, key):
        t = self.parameters['TURN']
        d = self.parameters['RESOURCE'][t][self.language]
        if key in d:
            s = d[key]
        else:
            t = 'BOTH'
            d = self.parameters['RESOURCE'][t][self.language]
            s = d[key]
        #print 'Using resource text <%s>.' % s
        return s

    def files(self, key):
        return self.parameters['FILES'][key]

    def colors(self, role, key):
        return self.parameters['COLORS'][role][key]

    def __init__(self, lang, param):
        InvestmentGameFullScreen.__init__(self)
        self.last = False
        self.language = lang
        self.running = True
        self.written = None
        self.parameters = param
        self.selectionText = StringVar()
        self.originalText = StringVar()
        self.availableText = StringVar()
        self.commentText = StringVar()
        self.originalAmount = StringVar()
        self.availableAmount = StringVar()
        self.selectionAmount = StringVar()
        self.profile = Label(self, image = None)
        self.slider = sld.InvestmentGameSlider(self, None)
        self.slider.bind('<ButtonRelease-1>', self.pickValue)

        if self.parameters['message']:
            self.commentLabel = \
                Label(self, textvariable = self.commentText, \
                          font = ('Helvetica', 18))
            self.comments = \
                Text(self, font = ('Helvetica', 20), width = 40, height = 6)

        self.selectionLabel = \
            Label(self, textvariable = self.selectionText, font = ('Helvetica', 24))
        self.selectionValue = \
            Label(self, textvariable = self.selectionAmount, font = ('Helvetica', 24))
        self.availableLabel = \
            Label(self, textvariable = self.availableText, font = ('Helvetica', 24))
        self.availableValue = \
            Label(self, textvariable = self.availableAmount, font = ('Helvetica', 24))
        self.originalValue = \
            Label(self, textvariable = self.originalAmount, font = ('Helvetica', 24))
        self.originalLabel = \
            Label(self, textvariable = self.originalText, font = ('Helvetica', 24))
        self.button = Button(self, \
                                 text = self.resource('CONTINUE'), \
                                 font = ('Helvetica', 16), \
                                 fg = 'black', activeforeground = 'black')
        self.button.bind('<Button-1>', self.done)
        self.target = None
        self.wait = ldr.Loader(self, self.parameters['FILES']['LOADER'])
        self.layout()
        return

    def stall(self, prop):
        #print 'Stalling...'
        self.randomDelay(round(100 * prop))
        return
            
    def randomDelay(self, selectionPercentage):
        ref = fabs(selectionPercentage - 50)
        rounds = 50 + randint(0, ref + 10)
        #print 'Waiting %d rounds' % rounds
        if self.parameters['message']:
            self.comments.configure(state = DISABLED)
            self.button.configure(state = DISABLED)
        self.slider.disable()
        self.wait.animate(rounds, self)
        return

    def signal(self):
        #print 'Stall stop signal received.'
        self.target.signal()
        return

    def background(self, bg):
        self.slider.background(bg)
        if self.parameters['message']:
            self.commentLabel.configure(background = bg)
        self.button.configure(highlightbackground = bg)#, foreground = bg)
        self.selectionLabel.configure(background = bg)
        self.selectionValue.configure(background = bg)
        self.availableLabel.configure(background = bg)
        self.availableValue.configure(background = bg)
        self.originalLabel.configure(background = bg)
        self.originalValue.configure(background = bg)
        self.wait.configure(background = bg)
        self.configure(background = bg)
        #print 'Background colors are set.'
        return

    def stop(self):
        self.wait.stop()

    def done(self, event):
        if self.parameters['message']:
            text = self.comments.get(1.0, END).encode("ISO-8859-1")
            self.written = text
        self.target.done(self.slider.get())
        if self.last:
            print 'Final round concluded.'
            self.disableAll()
        return

    def pickValue(self, event):
        # print 'Picking a value on a slider.'
        self.slider.update()
        self.target.pickValue(self.slider.get())
        (ct, cv) = self.target.setSelection()
        self.selectionText.set(ct)
        self.selectionAmount.set(cv)
        return

    def layout(self):
        self.profile.grid(row = 0, column = 3, rowspan = 2, \
                              padx = 40, pady = 50, sticky = N+E)
        self.originalLabel.grid(row = 0, column = 0, columnspan = 2, \
                                    padx = 50, pady = 10, sticky = E)
        self.originalValue.grid(row = 0, column = 2, sticky = W)
        self.availableLabel.grid(row = 1, column = 0, columnspan = 2, \
                                     padx = 50, pady = 10, sticky = E)
        self.availableValue.grid(row = 1, column = 2, sticky = W)
        self.slider.grid(row = 2, column = 1, columnspan = 3, rowspan = 2, padx = 150)
        self.selectionLabel.grid(row = 4, column = 0, columnspan = 2, \
                                     padx = 50, pady = 10, sticky = E)
        self.selectionValue.grid(row = 4, column = 2, sticky = W)
        if self.parameters['message']:
            self.commentLabel.grid(row = 5, column = 0, columnspan = 2, \
                                       padx = 50, pady = 10, sticky = W)
            self.comments.grid(row = 6, column = 1, padx = 100, pady = 5, \
                                   sticky = S+N+E+W)
        self.wait.grid(row = 5, column = 3, padx = 20, pady = 20, sticky = S+E)
        self.button.grid(row = 6, column = 3, padx = 20, pady = 20, sticky = S+E)
        #print 'Window layout done.'
        return

    def round(self, role, r, t):
        self.last = (r + 1 == t)
        if r < t:
            self.title(self.resource('TITLE') + ': ' + \
                           self.resource(role) + \
                           ' (' + \
                           self.resource('ROUND') + \
                           (' %d / %d)' % (r + 1, t)))
        else:
            self.title(self.resource('SUMMARY'))
        return
