## Solving SAT problems using DPLL

This repository contains scripts for solving SAT problems using the Davis-Putnam-Logemann-Loveland algorithm.


### ./SAT.sh -heuristic DIMACSfile

The main program can be run from SAT.sh. It must be called with a **heuristic** and the relative path of a **DIMACS file**. Heuristics may be either of:

* `-S1` for the random branching strategy
* `-S2` for the MOMS heuristic
* `-S3` for the Jaroslaw-Wang one-sided heuristic
* `-S4` for the Jaroslaw-Wang two-sided heuristic
* `-S5` for the Nishio heuristic, explained in the paper accompanying this report.

DIMACS files must be provided in the conventional format (lines with c and p may be omitted). An example file is *sudoku_nr_14803.txt*.

Alternatively, the Python script may be called directly as `python SAT.py heuristic filename`, where `heuristic` is one of `MOMS, JW, JWTS, nishio, random`, and `filename` is the relative path to a DIMACS file.


### results

The folder 'results' contains experimental results from running the algorithm and its different heuristics on a set of Sudoku problems.

### scripts

The folder 'scripts' contains several scripts used in the analysis of the obtained results.

### sudokus

The folder 'sudokus' contains files with sudoku puzzles that can be converted to DIMACS format with `scripts/clean_DIMACS.py`.
