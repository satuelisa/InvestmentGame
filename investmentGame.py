# -*- coding: utf-8 -*-
from time import time, sleep
from sys import argv
from random import randint
#import locale
import investmentGameController as ctrl
import investmentGameModel as model
import investmentGameRound as rnd
import investmentGameWindow as wnd

# version actual

NAMES = ['gain', 'investor', 'trustee', 'initialCapital', 'capitalIncrement', \
             'rounds', 'resetCapital', 'language', 'deviation']
    
def parseResource(resourceFile):
    r = dict()
    r['INVESTOR'] = dict()
    r['TRUSTEE'] = dict()
    r['BOTH'] = dict()
    for k in r.keys():
        r[k]['EN'] = dict() # English
        r[k]['ES'] = dict() # Spanish
    input = open(resourceFile, 'r')
    for line in input.readlines():
        line = line.strip()
        if len(line) > 0:
            tokens = line.split()
            if len(tokens) > 3:
                role = tokens.pop(0)
                language = tokens.pop(0)
                string = tokens.pop(0)
                value = ' '.join(tokens)
                r[role][language][string] = value
            else:
                print 'Incomplete resource line <%s>.' % \
                    line
    input.close()
    return r

def parseFiles(file):
    input = open(file)
    result = dict()
    for line in input.readlines():
        line = line.strip()
        if len(line) > 0:
            tokens = line.split()
            if len(tokens) == 2:
                result[tokens[0]] = tokens[1]
    input.close()
    return result

def parseColors(filename):
    result = dict()
    result['INVESTOR'] = dict()
    result['TRUSTEE'] = dict()
    input = open(filename, 'r')
    for line in input.readlines():
        line = line.strip()
        if len(line) > 0:
            tokens = line.split()
            if len(tokens) == 3:
                result[tokens[0]][tokens[1]] = tokens[2]
    input.close()
    return result

def parseConfig(configurationFile):
    global NAMES
    parameters = dict()
    input = open(configurationFile, 'r')
    for line in input.readlines():
        line = line.strip()
        if len(line) > 0:
            tokens = line.split()
            if len(tokens) == 3:
                variable = tokens.pop(0)
                type = tokens.pop(0)
                value = tokens.pop(0)
                try:
                    if type == 'bool':
                        parameters[variable] = (value == 'True')
                    elif type == 'char':
                        parameters[variable] = value[0]
                    else:
                        converter = vars(__builtins__)[type]
                        parameters[variable] = converter(value)
                except:
                    print '<%s> cannot be interpreter as type <%s>' % (value, type)
                    print 'Variable %s is not properly set.' % variable
            else:
                print 'Skipping incorrect config line <%s>.' % line
    input.close()
    for n in NAMES:
        if n not in parameters:
            print 'Variable <%s> undefined.' % n
    parameters['RESOURCE'] = parseResource('investmentGame.resource')
    parameters['FILES'] = parseFiles('investmentGame.files')
    parameters['COLORS'] = parseColors('investmentGame.colors')
    parameters['TURN'] = 'BOTH'
    return parameters

def main():
    #locale.setlocale(locale.LC_ALL, 'es_ES')
    parameters = parseConfig('investmentGame.cfg')
    if parameters['investor'] == 'X' or parameters['trustee'] == 'X':
        window = wnd.InvestmentGameWindow(parameters['language'], parameters)
    else:
        window = None
    logfile = 'investmentGame.' + str(int(time())) + '.log'
    controller = ctrl.Controller(window, parameters, logfile)
    if window is not None:
        print 'Esperando a la otra persona...'
        sleep(2 + randint(2, 5))
        window.after(10, controller.run)
        window.mainloop()
    else:
        controller.run()
    return

if __name__ == '__main__':
    main()
