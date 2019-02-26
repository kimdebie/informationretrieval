## Solving SAT problems using DPLL

This repository contains scripts for solving SAT problems using the Davis-Putnam-Logemann-Loveland algorithm.

### SAT.py [heuristic] [DIMACSfile]

The main program can be found in SAT.py. It must be called with a **heuristic** and the relative path of a **DIMACS file**. Heuristics may be either of:

* `JW` for the Jaroslaw-Wang one-sided heuristic
* `JWTS` for the Jaroslaw-Wang two-sided heuristic
* `MOM` for the MOMs heuristic
* `nishio` for the Nishio heuristic, explained in the paper accompanying this report.

DIMACS files must be provided in the conventional format (lines with c and p may be omitted). An example file is *sudoku_nr_14261.txt*.


### results

The folder 'results' contains experimental results from running the algorithm and its different heuristics on a set of Sudoku problems.

### scripts

The folder 'scripts' contains several scripts used in the analysis of the obtained results.

### sudokus

The folder 'sudokus' contains files with sudoku puzzles that can be converted to DIMACS format with `scripts/clean_DIMACS.py`.
