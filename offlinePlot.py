import matplotlib.pyplot as plt
from sys import argv

logfile = None
try:
    logfile = argv[1]
except:
    print 'Define el archivo .log a graficar'
    quit()

investor = list()
trustee = list()
highlightX = list()
highlightY = list()
n = 0
input = open(logfile, 'r')
for line in input.readlines():
    tokens = line.split()
    if tokens[0] == '#':
        continue
    else:
        capital = float(tokens[1])
        invested = float(tokens[5])
        gain = float(tokens[6])
        returned = float(tokens[10])
        percInv = 100.0 * invested / capital
        percTru = 100.0 * returned / gain
        investor.append(percInv)
        trustee.append(percTru)
        n += 1
        if returned <= invested:
            highlightX.append(n)
            highlightY.append(percTru)
plt.clf()

fig = plt.subplot(111)
x = range(1, n + 1)
plt.ylim(-5, 105)
plt.xlim(0.5, n + 0.5)
plt.title('Porcentaje invertido/regresado por ronda')
plt.plot(x, trustee, 'g-', linewidth = 3, \
             label = 'El porcentaje que regresaste')
plt.plot(x, investor, 'b-', linewidth = 3, \
             label = 'El porcentaje invertido por la otra persona')
plt.scatter(highlightX, highlightY, s = 128, color='orange')
plt.scatter(x, trustee, s = 32, color = 'green')
plt.scatter(x, investor, s = 32, color = 'blue')
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(20))

box = fig.get_position()
fig.set_position([box.x0, box.y0 + box.height * 0.1,
                  box.width, box.height * 0.9])

fig.legend(loc = 'upper center', bbox_to_anchor=(0.5, -0.05),
           fancybox = True, shadow = True, ncol = 1)

plt.savefig(logfile[:-4] + '_offline.png')
plt.show()



