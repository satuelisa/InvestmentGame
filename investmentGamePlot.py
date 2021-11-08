# http://stackoverflow.com/questions/732192/get-tk-winfo-rgb-without-having-a-window-instantiated indica los hex de los colores de tkinter
# http://ajaxload.info/ es lo que genera la ruedita de espera

from Tkinter import *
import matplotlib.pyplot as plt
import investmentGameRound as rnd

class InvestmentGamePlot:
    def __init__(self, history, filename):

        investor = list()
        trustee = list()
        highlightX = list()
        highlightY = list()
        n = 0
        for round in history:
            investor.append(round.getValue(rnd.INVESTOR) * 100.0)
            percTru = round.getValue(rnd.TRUSTEE) * 100.0
            trustee.append(percTru)
            n += 1
            if round.getValue(rnd.TRUSTEE, True) < round.getValue(rnd.INVESTOR, True):
                highlightX.append(n)
                highlightY.append(percTru)

        plt.clf()

        fig = plt.subplot(111)

        plt.ylim(-5, 105)
        plt.xlim(0.5, n + 0.5)
        plt.title('Porcentaje invertido/regresado por ronda')
        x = range(1, n + 1)
        plt.plot(x, trustee, 'g-', linewidth = 3, \
                     label = 'El porcentaje que regresaste')
        plt.plot(x, investor, 'b-', linewidth = 3, \
                     label = 'El porcentaje invertido por la otra persona')
        plt.scatter(highlightX, highlightY, s = 128, color='orange')
        plt.scatter(x, trustee, s = 32, color = 'g')
        plt.scatter(x, investor, s = 32, color = 'b')
        plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
        plt.gca().yaxis.set_major_locator(plt.MultipleLocator(20))

        box = fig.get_position()
        fig.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.9])

        fig.legend(loc = 'upper center', bbox_to_anchor=(0.5, -0.05),
                  fancybox = True, shadow = True, ncol = 1)

        plt.savefig(filename)
        plt.show()
        return


