from time import time, asctime, sleep
from random import uniform
from sys import exit
from subprocess import call
import investmentGameModel as game
import investmentGameModel as mdl
import investmentGameView as view
import investmentGameDialog as dlg
import investmentGamePlot as plt
import investmentGameRound as rnd
import investmentGameInfo as info
from math import floor
from Tkinter import *
import tkMessageBox

class Controller:

    def resource(self, key):
        return self.parameters['RESOURCE'][self.language][key]

    def __init__(self, w, param, log):
        self.parameters = param
        self.window = w
        self.logFile = log
        self.history = list()
        self.model = dict()
        self.model['INVESTOR'] = mdl.Investor(self.parameters['investor'], \
                                                self.parameters['deviation'])
        self.interface = dict()
        if self.parameters['investor'] == 'X': # human = GUI
            self.interface['INVESTOR'] = \
                view.InvestorInterface(self, self.window)
        self.model['TRUSTEE'] = mdl.Trustee(self.parameters['trustee'], \
                                              self.parameters['deviation'])
        if self.parameters['trustee'] == 'X':
            self.interface['TRUSTEE'] = \
                view.TrusteeInterface(self, self.window)
        self.capital = self.parameters['initialCapital']
        self.totalGain = None
        self.totalRounds = self.parameters['rounds']
        self.multiplier = self.parameters['gain']
        self.increment = self.parameters['capitalIncrement']
        self.clear = self.parameters['resetCapital']
        self.clicks = {'INVESTOR': 0, 'TRUSTEE': 0}
        self.delay = {'INVESTOR': 0, 'TRUSTEE': 0}
        self.selected = dict()
        self.totals =  {'INVESTOR': 0.0, 'TRUSTEE': 0.0}
        self.previous = dict()
        self.currentRound = 0
        self.waiting = False
        self.finished = False
        self.parameters['TURN'] = None
        self.availableCapital = None
        return

    def inTurn(self):
        return self.parameters['TURN']

    def proceed(self):
        #print 'Concluding round %d of %d.' % (self.currentRound , self.totalRounds)
        self.waiting = False
        if self.currentRound < self.totalRounds:
            self.parameters['TURN'] = 'INVESTOR'
            if self.window is not None:
                #print 'Control over to GUI...'
                self.window.after(10, self.play)
            else:
                #print 'Commencing a new round.'
                self.play()
        else:
            #print 'Finished.'
            self.finished = True
            if self.window is not None:
                self.window.after(10, self.plot)
            else:
                self.plot()
        return

    def done(self):
        self.clicks[self.expected] = self.interface[self.expected].clicks
        self.delay[self.expected] = self.interface[self.expected].delay
        self.selected[self.expected] = self.interface[self.expected].selectedAmount
        if self.expected == 'INVESTOR':
            #print 'Investor response received from GUI.'
            self.parameters['TURN'] = 'TRUSTEE'
        elif self.expected == 'TRUSTEE':
            #print 'Trustee response received from GUI.'
            self.parameters['TURN'] = None
        #else:
            #print 'Unexpected response received from GUI.'
        self.waiting = False
        if self.window is not None:
            #print 'Returning to GUI control...'
            self.window.after(0, self.next)
        else:
            #print 'Continuing...'
            self.next()
        return

    def display(self, type, values):
        if self.window is not None and not self.window.running:
            self.window.start()
        self.interface[type].play(values, self.currentRound, self.totalRounds)
        return

    def record(self):
        #print 'Recording round statistics.'
        inv = self.selected['TRUSTEE'] + (self.availableCapital - self.selected['INVESTOR'])
        trus = self.totalGain - self.selected['TRUSTEE']
        self.model['INVESTOR'].receive(self.selected['TRUSTEE'])
        self.model['TRUSTEE'].receive(trus)

        # agrega ronda
        self.history.append(rnd.Round(self.selected['INVESTOR'], self.availableCapital, \
                                          self.selected['TRUSTEE'], self.totalGain))

        # actualiza totales
        self.totals['INVESTOR'] += inv
        self.totals['TRUSTEE'] += trus 

        # escribel log
        print >>self.log, '%2d %8.2f\t%8.2f\t%d\t%d\t%8.2f %8.2f\t%8.2f\t%d\t%d\t%8.2f\t%8.2f' % \
            (self.currentRound, self.availableCapital, self.model['INVESTOR'].capital, \
                 self.clicks['INVESTOR'], self.delay['INVESTOR'], self.selected['INVESTOR'], \
                 self.totalGain, self.model['TRUSTEE'].capital, \
                 self.clicks['TRUSTEE'], self.delay['TRUSTEE'], self.selected['TRUSTEE'], \
                 self.totalGain - self.selected['TRUSTEE'])

        if self.parameters['message']:
            if self.window is not None and len(self.window.written) > 0:
                print >>self.log, '# C %s' % self.window.written
        return

    def relativeRound(self):
        return int(floor(10.0 * (self.currentRound - 1.0) / self.totalRounds))

    def investor(self):
        #print 'Investor has turn.'
        self.model['INVESTOR'].receive(self.increment)
        self.availableCapital = self.model['INVESTOR'].capital
        if 'INVESTOR' in self.interface:
            self.expected = 'INVESTOR'
            self.waiting = True
            self.display('INVESTOR', [self.availableCapital])
        else:
            self.selected['INVESTOR'] = self.model['INVESTOR'].play(self.relativeRound(), self.history)
            if self.totalGain is not None: # if not on the first round
                if 'TRUSTEE' in self.interface:
                    self.waiting = True
                    #print 'Delay for investor model decision making.'
                    if 'TRUSTEE' in self.previous:
                        self.window.stall(self.previous['TRUSTEE'] / self.totalGain)
                    else:
                        self.window.stall(0.5) # for the first round
            self.parameters['TURN'] = 'TRUSTEE'
            self.next()
        return

    def trustee(self):
        #print 'Trustee has turn.'
        self.model['INVESTOR'].withdraw(self.selected['INVESTOR'])
        self.totalGain = self.multiplier * self.selected['INVESTOR']
        if 'TRUSTEE' in self.interface:
            self.expected = 'TRUSTEE'
            self.waiting = True
            self.display('TRUSTEE', \
                             [self.selected['INVESTOR'], \
                                  self.availableCapital, \
                                  self.totalGain])
        else:
            if 'INVESTOR' in self.interface:
                self.waiting = True
                #print 'Delay for trustee model decision making.'
                if 'INVESTOR' in self.selected:
                    self.window.stall(self.selected['INVESTOR'] / self.availableCapital)
                else:
                    self.window.stall(0.5) # for the first round
            self.selected['TRUSTEE'] = \
                self.model['TRUSTEE'].play(self.relativeRound(), self.totalGain, self.history)
            self.parameters['TURN'] = None
            self.next();
        return
                    
    def summary(self):
        if 'INVESTOR' in self.interface \
                or 'TRUSTEE' in self.interface:
            self.waiting = True
            #print 'Displaying round summary.'
            if len(self.interface.keys()) == 2:
                role = 'BOTH'
            elif 'INVESTOR' in self.interface:
                role = 'INVESTOR'
            else:
                role = 'TRUSTEE'
            self.parameters['TURN'] = role
            #print 'Displaying the summary for %s.' % role
            dlg.InvestmentGameDialog(self,
                                     self.window, role, \
                                         (self.availableCapital, \
                                              self.selected['INVESTOR'], \
                                              self.totalGain, \
                                              self.selected['TRUSTEE'], \
                                              self.model['INVESTOR'].balance(), \
                                              self.model['TRUSTEE'].balance()), 
                                     self.clear)
            return True
        return False


    def next(self):
        if self.waiting:
            self.window.after(100, self.next)
            #print 'Waiting for the stall to end.'
            return
        if self.parameters['TURN'] == 'INVESTOR':
            self.investor()
            return
        elif self.parameters['TURN'] == 'TRUSTEE':
            self.trustee()
            return
        else:
            #print 'Both players have made their choices.'
            auto = False
            if not self.summary():
                auto = True
            self.record()
            self.currentRound += 1
            if auto:
                self.proceed()
        return

    def play(self):
        if self.clear:
            #print 'Clearing capitals.'
            self.model['INVESTOR'].reset(0.0)
            self.model['TRUSTEE'].reset(0.0)
            if len(self.selected.keys()) == 2:
                self.previous = [self.selected['INVESTOR'], self.selected['TRUSTEE']]
            self.selected = dict()
        #print 'Ready for a new round.'        
        self.parameters['TURN'] = 'INVESTOR'
        if self.window is not None:
            #print 'Control over to GUI...'
            self.window.after(10, self.next)
        else:
            #print 'Starting.'
            self.next()
        return

    def run(self):
        self.log = open(self.logFile, 'w')
        print >>self.log, '# Timestamp:', asctime()
        print >>self.log, \
            '# Capital\tAvailable\tClicks\tTime\tSelected\tGain\tTotal\t\tClicks\tTime\tReturned\tKept'
#        print 'Game begins.'
        if self.window is not None:
            self.window.after(10, self.play)
        else:
            self.play()
        return

    def finish(self):
        try:
            self.window.finish()
            self.window.quit()
            self.window.destroy()
        except:
            pass
        self.log.close()
        print 'Juego terminado'        
        exit()

    def plot(self):
        # falta agregar analisis	
        print 'Archivo de registro: %s.' % self.logFile
        print 'Graficando el historial de juego.'
        info.InvestmentGameInfo(self, self.window, \
                                (self.totals['INVESTOR'], self.totals['TRUSTEE']), \
                                     self.logFile, \
                                     self.parameters['finalMessage'])
        plt.InvestmentGamePlot(self.history, self.logFile[:-4] + '.png')
        return

