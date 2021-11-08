set term postscript eps 20 color
set output "models.eps"
set pointsize 1.5
set key at 10, 0.93
set xlabel "Round"
set ylabel "Proportion"
set size 4,4
set xtics 1 ,1
set ytics 0 ,0.1
set xrange [0.5:10.5]
set yrange [-0.05:1.05]
set multiplot
set size 0.9, 1
set origin 0, 3
set title "A = Cluster 1: ADHD subjects"
plot "investor.dat" using 1:2 title "Investor" with linespoints pt 7 lt 1, \
"trustee.dat" using 1:2 title "Trustee" with linespoints pt 5 lt 2
set origin 1, 3
set title "B = Cluster 2: adolescents with ASD as investors"
plot "investor.dat" using 1:3 title "Investor" with linespoints pt 7 lt 1, \
"trustee.dat" using 1:3 title "Trustee" with linespoints pt 5 lt 2
set origin 2, 3
set title "C = Cluster 3: medicated and non-medicated BPD"
plot "investor.dat" using 1:4 title "Investor" with linespoints pt 7 lt 1, \
"trustee.dat" using 1:4 title "Trustee" with linespoints pt 5 lt 2
set origin 3, 3
set title "D = Cluster 4: MDD subjects as investors"
plot "investor.dat" using 1:5 title "Investor" with linespoints pt 7 lt 1, \
"trustee.dat" using 1:5 title "Trustee" with linespoints pt 5 lt 2
set origin 0, 2
set title "E = Socioeconomically matched controls for BPD subjects"
plot "investor.dat" using 1:6 title "Investor" with linespoints pt 7 lt 1, \
"trustee.dat" using 1:6 title "Trustee" with linespoints pt 5 lt 2
set origin 1, 2
set title "F = High-functioning males with ASD"
plot "investor.dat" using 1:7 title "Investor" with linespoints pt 7 lt 1, \
"trustee.dat" using 1:7 title "Trustee" with linespoints pt 5 lt 2
set origin 2, 2
set title "G = Parents of high-functioning males with ASD"
plot "investor.dat" using 1:8 title "Investor" with linespoints pt 7 lt 1, \
"trustee.dat" using 1:8 title "Trustee" with linespoints pt 5 lt 2
set origin 3, 2
set title "H = Children with ADHD, age/IQ-matched to ASD males"
plot "investor.dat" using 1:9 title "Investor" with linespoints pt 7 lt 1, \
"trustee.dat" using 1:9 title "Trustee" with linespoints pt 5 lt 2
set origin 0, 1
set title "I = Parents of children with ADHD"
plot "investor.dat" using 1:10 title "Investor" with linespoints pt 7 lt 1, \
"trustee.dat" using 1:10 title "Trustee" with linespoints pt 5 lt 2
set origin 1, 1
set title "J = Age/IQ-matched controls for high-functioning males with ASD"
plot "investor.dat" using 1:11 title "Investor" with linespoints pt 7 lt 1, \
"trustee.dat" using 1:11 title "Trustee" with linespoints pt 5 lt 2
set origin 2, 1
set title "K = Parents of controls for high-functioning ASD males"
plot "investor.dat" using 1:12 title "Investor" with linespoints pt 7 lt 1, \
"trustee.dat" using 1:12 title "Trustee" with linespoints pt 5 lt 2
set origin 3, 1
set title "L = MDD subjects, psychiatric controls for BPD subjects"
plot "investor.dat" using 1:13 title "Investor" with linespoints pt 7 lt 1, \
"trustee.dat" using 1:13 title "Trustee" with linespoints pt 5 lt 2
set origin 0, 0
set title "M = Impersonal task, healthy subjects who did not meet before playing"
plot "investor.dat" using 1:14 title "Investor" with linespoints pt 7 lt 1, \
"trustee.dat" using 1:14 title "Trustee" with linespoints pt 5 lt 2
