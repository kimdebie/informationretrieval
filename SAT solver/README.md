To do:
* Run each heuristic
* Come up with script for analysis


Analysis
- test the relative level of performance of each of the heuristics
- across each of the levels of difficulty
- level of performance is:
Being good at finding the correct path: few number of backtracks
Getting to the solution quickly: small number of guesses


Test if what was hard under the random distribution is still hard under the heuristics.

Hardness score: guesses + backtracks
Scatterplot: xaxis hardness score for random, yaxis hardness score for heuristic
If a point is high on the xaxis and high on the yaxis, it is difficult under the heuristic as well as under random
If it is low on both, it is always easy
If a point is high on the xaxis and low on the yaxis, it is difficult under random, but easy under heuristic
If a point is low on xaxis and high on yaxis, it is more difficult under the heuristic than under random.
Interested in RELATIVE performance; so the axes are scaled to their relative domains. Alternative: hardness RANK instead of hardness score. 
