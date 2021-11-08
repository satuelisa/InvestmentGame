# http://stackoverflow.com/questions/732192/get-tk-winfo-rgb-without-having-a-window-instantiated indica los hex de los colores de tkinter
# http://ajaxload.info/ es lo que genera la ruedita de espera

from Tkinter import *
import investmentGameWindow as wnd
import investmentGameSlider as sld
import investmentGameView as view

INVESTOR = 0
TRUSTEE = 1
MAX_LENGTH = 500
        
class InvestmentGameDialog:
    def __init__(self, controller, parent, role, values, reset):
        global INVESTOR, TRUSTEE, MAX_LENGTH
        self.top = Toplevel(parent)
        padding = 5
        w = self.top.winfo_screenwidth() - padding
        h = self.top.winfo_screenheight() - padding
        self.top.geometry('{0}x{1}+0+0'.format(w, h))
 
        self.controller = controller
        original = values[0]
        inversion = values[1]
        gain = values[2]
        returned = values[3]
        invBalance = values[4]
        trusBalance = values[5]
        kept = gain - returned
        savings = original - inversion
        total = savings + returned
        trusNewBalance = trusBalance + kept
        
        self.top.configure(bg = parent.colors('INVESTOR', 'SUMMARY'))

        norm = max(gain, original, total, trusNewBalance)
        unit = MAX_LENGTH / (norm * 1.0)

        label = Label(self.top, text = parent.resource('SUMMARY'), \
                          font = ('Helvetica', 24))
        label.configure(bg = parent.colors('INVESTOR', 'SUMMARY'))
        label.grid(row = 0, column = 0, columnspan = 4, padx = 50, pady = 50, sticky = W)

        label = Label(self.top, text = parent.resource('INVERSION'), \
                          font = ('Helvetica', 18))
        label.configure(bg = parent.colors('INVESTOR', 'SUMMARY'))
        label.grid(row = 1, column = 0, padx = 30, pady = 30, sticky = W)

        lc = parent.colors('INVESTOR', 'INVEST')
        rc = parent.colors('INVESTOR', 'KEEP')
        capital = sld.InvestmentGameSlider(self.top, view.formatAmount(original))
        capital.setup(original, lc, rc, int(round(unit * original)))
        capital.set(inversion)
        capital.disable()
        capital.background(parent.colors('INVESTOR', 'SUMMARY'))
        capital.grid(row = 1, column = 1, rowspan = 2, columnspan = 3, sticky = W)
        
        label = Label(self.top, text = parent.resource('PROFIT'), \
                          font = ('Helvetica', 18))
        label.configure(bg = parent.colors('INVESTOR', 'SUMMARY'))
        label.grid(row = 3, column = 0, padx = 30, pady = 30, sticky = W)
        
        lc = parent.colors('TRUSTEE', 'RETURN')
        rc = parent.colors('TRUSTEE', 'KEEP') 
        generated = sld.InvestmentGameSlider(self.top, view.formatAmount(gain))
        generated.setup(gain, lc, rc, int(round(unit * gain)))
        if gain > 0:
            generated.set(gain - kept)
        else:
            generated.set(0)
        generated.disable()
        generated.background(parent.colors('INVESTOR', 'SUMMARY'))
        generated.grid(row = 3, column = 1, rowspan = 2, columnspan = 3, sticky = W)

        label = Label(self.top, text = parent.resource('EARNINGS'), \
                          font = ('Helvetica', 18))
        label.configure(bg = parent.colors('INVESTOR', 'SUMMARY'))
        label.grid(row = 5, column = 0, padx = 30, pady = 30, sticky = W)
        
        lc = parent.colors('INVESTOR', 'KEEP')
        rc = parent.colors('TRUSTEE', 'RETURN')   
        investor = sld.InvestmentGameSlider(self.top, view.formatAmount(total))
        investor.setup(total, lc, rc, int(round(unit * total)), value = False)
        investor.set(savings)
        investor.disable()
        investor.background(parent.colors('INVESTOR', 'SUMMARY'))
        investor.grid(row = 5, column = 1, rowspan = 2, columnspan = 3, sticky = W)
        
        label = Label(self.top, text = parent.resource('TBALANCE'), \
                          font = ('Helvetica', 18))
        label.configure(bg = parent.colors('INVESTOR', 'SUMMARY'))
        label.grid(row = 7, column = 0, padx = 30, pady = 30, sticky = W)

        rc = parent.colors('TRUSTEE', 'TOTAL')
        lc = parent.colors('TRUSTEE', 'KEEP')
        trusteeTot = sld.InvestmentGameSlider(self.top, view.formatAmount(trusNewBalance))
        trusteeTot.setup(trusNewBalance, lc, rc, int(round(unit * trusNewBalance)), value = False)
        trusteeTot.set(kept)
        trusteeTot.disable()
        trusteeTot.background(parent.colors('INVESTOR', 'SUMMARY'))
        trusteeTot.grid(row = 7, column = 1, rowspan = 2, columnspan = 3, sticky = W)
            
        button = Button(self.top, \
                            text = parent.resource('CONTINUE'), \
                            font = ('Helvetica', 16), \
                            fg = 'black', activeforeground = 'black')
        button.bind('<Button-1>', self.ack)
        button.configure(highlightbackground = parent.colors('INVESTOR', 'SUMMARY'))
        #foreground = parent.colors('INVESTOR', 'SUMMARY'))

        button.grid(row = 9, column = 1, columnspan = 1, padx = 30, pady = 30, sticky = W)
        return
        
    def ack(self, event):
        self.controller.proceed()
        self.top.destroy()
        return
        


