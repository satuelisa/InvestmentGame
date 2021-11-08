from time import time, asctime, sleep
from random import uniform, gauss
from math import floor, sqrt
from investmentGameData import PROPORTION

INVESTOR = 0
TRUSTEE = 1
ROUNDS = 2

def bestMatch(type, currentRound, history):
    compare = range(ROUNDS) # based on last two
    minDist = float('inf')
    mean = None
    chosen = None
    for behavior in PROPORTION.keys():
        # print 'Considering %c for round %d' % (behavior, currentRound + 1)
        dist = 0.0
        for step in compare:
            past = history[-1 * (step + 1)].getValue(type) 
            rnd = currentRound - step - 1
            modeled = PROPORTION[behavior][type][rnd]
            # print 'Modeled: %.2f (round %d), Recorded: %.2f' % (modeled, rnd + 1, past)
            dist += (modeled - past)**2
        dist = sqrt(dist)
        if dist < minDist:
            minDist = dist
            mean = PROPORTION[behavior][type][currentRound]
            chosen = behavior
    #print 'Chose %c' % chosen
    return mean

class Player:

    def __init__(self, c, sd):
        self.cluster = c
        self.stdDev = sd
        self.capital = 0

    def receive(self, amount):
        if amount is not None:
            #print 'Deposited %d.' % amount
            self.capital += amount
        return

    def withdraw(self, amount):
        self.capital -= amount
        return

    def reset(self, c):
        self.capital = c
        return

    def balance(self):
        return self.capital

    def play(self, type, currentRound, history):
        global INVESTOR, TRUSTEE
        if self.cluster == 'Y': # adaptive response
            if currentRound < 2:
                mean = PROPORTION['M'][type][currentRound - 1]
            else:
                if type == INVESTOR:
                    other = TRUSTEE
                elif type == TRUSTEE:
                    other = INVESTOR
                else:
                    return None # error
                mean = bestMatch(other, currentRound, history)
        else: # curve-based response
            mean = PROPORTION[self.cluster][type][currentRound - 1]
        prop = gauss(mean, mean * self.stdDev)
        if prop < 0.0:
            return 0.0
        elif prop > 1.0:
            return 1.0
        else:
            return prop

class Investor(Player):
    def play(self, currentRound, history):
        global INVESTOR
        prop =  Player.play(self, INVESTOR, currentRound, history)
        return int(floor(prop * self.capital))

class Trustee(Player):
    def play(self, currentRound, available, history):
        global TRUSTEE
        prop = Player.play(self, TRUSTEE, currentRound, history)
        return int(floor(prop * available))

