# http://stackoverflow.com/questions/732192/get-tk-winfo-rgb-without-having-a-window-instantiated indica los hex de los colores de tkinter
# http://ajaxload.info/ es lo que genera la ruedita de espera

from Tkinter import *

INVESTOR = 0
TRUSTEE = 1

class InvestmentGameInfo:
    def __init__(self, controller, parent, values, log, msg):
        global INVESTOR, TRUSTEE
        
        self.log = log + '.msg'
        self.permitMessage = msg

        self.top = Toplevel(parent)
        padding = 5
        w = self.top.winfo_screenwidth() - padding
        h = self.top.winfo_screenheight() - padding
        self.top.geometry('{0}x{1}+0+0'.format(w, h))
        self.controller = controller

        self.top.title(parent.resource('FINALSUMMARY'))

        (inv, trus) = values

        invTotal = \
            '%s: %.0f' % (parent.resource('INVFINAL'), inv)

        trusTotal = \
            '%s: %.0f' % (parent.resource('TRUSFINAL'), trus)

        self.top.configure(bg = parent.colors('INVESTOR', 'SUMMARY'))

        label = Label(self.top, text = invTotal, 
                          font = ('Helvetica', 24))
        label.configure(bg = parent.colors('INVESTOR', 'SUMMARY'))
        label.grid(row = 0, column = 0, columnspan = 1, \
                       padx = 50, pady = 50, sticky = W)


        label = Label(self.top, text = trusTotal, 
                          font = ('Helvetica', 24))
        label.configure(bg = parent.colors('INVESTOR', 'SUMMARY'))
        label.grid(row = 1, column = 0, columnspan = 1, \
                       padx = 50, pady = 50, sticky = W)

        if self.permitMessage:
            print 'Pidiendo mensaje final.'
            label = \
                Label(self.top, text = parent.resource('FINALMESSAGE'), \
                          font = ('Helvetica', 18))
            label.configure(bg = parent.colors('INVESTOR', 'SUMMARY'))
            self.comments = \
                Text(self.top, font = ('Helvetica', 20), width = 40, height = 6)
            label.grid(row = 3, column = 0, columnspan = 1, \
                                       padx = 50, pady = 10, sticky = W)
            self.comments.grid(row = 4, column = 0, padx = 100, pady = 5, \
                                   sticky = S+N+E+W)
            
        self.button = Button(self.top, \
                            text = parent.resource('FINISH'), \
                            font = ('Helvetica', 16), \
                            fg = 'black', activeforeground = 'black')
        self.button.bind('<Button-1>', self.ack)
        self.button.configure(highlightbackground = parent.colors('INVESTOR', 'SUMMARY'))
        self.button.grid(row = 5, column = 0, columnspan = 1, \
                        padx = 30, pady = 30, sticky = W)
        return
        
    def ack(self, event):        
        if self.permitMessage:
            text = self.comments.get(1.0, END).encode("ISO-8859-1")
            text = text.strip()
            if len(text) > 0:
                input = open(self.log, 'w')
                print >>input, text
                input.close()
        self.button.config(state=DISABLED);
        self.comments.config(state=DISABLED);
        print 'Terminando el programa.'
#        self.controller.finish()
#        self.top.destroy()
        return
        


