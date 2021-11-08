input = open('models.raw', 'r')
columns = list()
titles = list()
for line in input.readlines():
    line = line.strip()
    if len(line) == 0:
        continue
    tokens = line.split()
    id = tokens.pop(0)
    if id == 'INVESTOR':
        pair = list()
        data = list()
        for t in tokens:
            data.append(float(t))
        pair.append(data)
    elif id == 'TRUSTEE':
        data = list()
        for t in tokens:
            data.append(float(t))
        pair.append(data)
        columns.append(pair)
        pair = None
    else:
        titles.append(' '.join(tokens))
input.close()
investor = open('investor.dat', 'w')
trustee = open('trustee.dat', 'w')
n = len(columns[0][0])
k = len(titles)
for j in xrange(n):
    si = '%d\t' % (j + 1)
    st = '%d\t' % (j + 1)
    for i in xrange(k):
        si += '%f\t' % columns[i][0].pop(0)
        st += '%f\t' % columns[i][1].pop(0)
    print >>investor, si
    print >>trustee, st
investor.close()
trustee.close()
output = open('models.plot', 'w')
print >>output, 'set term postscript eps 20 color'
print >>output, 'set output "models.eps"'
print >>output, 'set pointsize 1.5'
print >>output, 'set key at 10, 0.93'
print >>output, 'set xlabel "Round"'
print >>output, 'set ylabel "Proportion"'
print >>output, 'set size 4,4'
print >>output, 'set xtics 1 ,1'
print >>output, 'set ytics 0 ,0.1'
print >>output, 'set xrange [0.5:10.5]'
print >>output, 'set yrange [-0.05:1.05]'
print >>output, 'set multiplot'
print >>output, 'set size 0.9, 1'

row = 3
col = 0
for i in xrange(k):
    print >>output, 'set origin %d, %d' % (col, row)
    print >>output, 'set title "%s"' % titles.pop(0)
    col += 1
    if col == 4:
        col = 0
        row -= 1
    print row, col
    print >>output, 'plot "investor.dat" using 1:%d title "Investor" with linespoints pt 7 lt 1, \\' % (i + 2)
    print >>output, '"trustee.dat" using 1:%d title "Trustee" with linespoints pt 5 lt 2' % (i + 2)
output.close()

