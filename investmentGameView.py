from Tkinter import *
from time import time
from random import randint
from PIL import Image, ImageTk
from math import fabs, floor
import investmentGameWindow as wnd

SLIDER_WIDTH = 600
LENGTH = 5

def formatAmount(amount):
    global LENGTH
    s = '%.0f' % amount
    while len(s) < LENGTH:
        s = ' ' + s
    return ' $' + s + ' '

class Interface:

    def signal(self):
        self.controller.waiting = False
        #print 'Controller no longer waiting.'
        return

    def __init__(self, c, w):
        self.controller = c
        self.window = w
        self.start = None
        self.clicks = 0
        self.selectedAmount = None
        self.availableAmount = None
        self.profilePicture = None
        return
    
    def loadProfilePicture(self, type):
        if type == 'INVESTOR':
            imagefile = self.window.files('INVESTOR')
        elif type == 'TRUSTEE':
            imagefile = self.window.files('TRUSTEE')
        else:
            return
        #print 'Reading profile picture from %s.' % imagefile
        image = Image.open(imagefile)
        (w0, h0) = image.size
        mw = int(self.window.files('MAXWIDTH')) 
        mh = int(self.window.files('MAXHEIGHT')) 
        if w0 > mw or h0 > mh:
            pw = mw / float(w0)
            ph = mh / float(h0)
            if pw > ph: # scale w.r.t. to the width
                w = mw
                h = int(floor(h0 * pw))
            else:
                h = mh
                w = int(floor(w0 * ph))
        image = image.resize((w, h))
        self.profilePicture = ImageTk.PhotoImage(image)
        return

    def done(self, selection):
        #print 'User made a selection.'
        self.delay = time() - self.start
        if self.selectedAmount is None:
            self.selectedAmount = int(round((selection)))
        self.window.after(0, self.controller.done)
        return

    def pickValue(self, selection):
        self.clicks += 1
        self.selectedAmount = int(round((selection)))
        return

    def play(self, amount, rnd, tot):
        self.clicks = 0
        self.delay = None
        self.selectedAmount = 0.0
        self.availableAmount = amount
        self.start = time()
        self.round = rnd
        self.total = tot
        self.window.target = self
        self.window.profile.configure(image = self.profilePicture)
        self.window.profile.photo = self.profilePicture
        self.window.enableEditing()
        self.build()
        return

class InvestorInterface(Interface):

    def  __init__(self, c, w):
        Interface.__init__(self, c, w)
        self.loadProfilePicture('INVESTOR')
        return

    def play(self, amount, round, total):
        global SLIDER_WIDTH
        Interface.play(self, amount[0], round, total)
        self.window.slider.setup(self.availableAmount, \
                                     self.window.colors('INVESTOR', 'INVEST'), \
                                     self.window.colors('INVESTOR', 'KEEP'), \
                                     SLIDER_WIDTH, ticks = True)
        return

    def setSelection(self):
        return (self.window.resource('SELECTED') + \
                    ': ', formatAmount(self.selectedAmount))

    def build(self):
        #print 'Building the investor GUI.'
        self.window.round('INVESTOR', self.round, self.total)
        self.window.background(self.window.colors('INVESTOR', 'BACKGROUND'))
        self.window.originalText.set('')
        self.window.commentText.set(self.window.resource('COMMENT'))
        self.window.availableText.set(self.window.resource('CAPITAL'))
        self.window.availableAmount.set(formatAmount(self.availableAmount))
        (ct, cv) = self.setSelection()
        self.window.selectionText.set(ct)
        self.window.selectionAmount.set(cv)
        self.window.originalAmount.set('')
        #print 'GUI built.'
        return

class TrusteeInterface(Interface):

    def  __init__(self, c, w):
        Interface.__init__(self, c, w)
        self.loadProfilePicture('TRUSTEE')
        return

    def setSelection(self):
        return (self.window.resource('RETURN') + ' ', formatAmount(self.selectedAmount))

    def play(self, amount, round, total):
        global SLIDER_WIDTH
        self.investedAmount = amount[0]
        self.originalAmount = amount[1]
        Interface.play(self, amount[2], round, total)
        self.window.slider.setup(self.availableAmount, \
                                     self.window.colors('TRUSTEE', 'RETURN'), \
                                     self.window.colors('TRUSTEE', 'KEEP'), \
                                     SLIDER_WIDTH, ticks = True)
        return

    def build(self):
        #print 'Building the trustee GUI.'
        self.window.round('TRUSTEE', self.round, self.total)
        self.window.background(self.window.colors('TRUSTEE', 'BACKGROUND'))
        self.window.commentText.set(self.window.resource('COMMENT'))
        self.window.originalText.set(self.window.resource('INVEST') + \
                                         formatAmount(self.investedAmount) + ' ' + \
                                         self.window.resource('OUT_OF') + ' ' + \
                                         formatAmount(self.originalAmount))
        self.window.availableText.set(self.window.resource('GAIN'))
        self.window.availableAmount.set(formatAmount(self.availableAmount))
        (ct, cv) = self.setSelection()
        self.window.selectionText.set(ct)
        self.window.selectionAmount.set(cv)
        #print 'GUI built.'
        return

