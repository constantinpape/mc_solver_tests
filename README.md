# Multicut Solver Tests

Compare different multicut solver:
* Opengm Ilp-Solver and Fusion-Moves solver
* Nifty Ilp-Solver and Fusion-Moves solver
* LP_MP Multicut solver

## Opengm vs nifty

On cremi problems from training samples:

| Solver        | Sample A  | Sample B  | Sample C  |
|-------------  | -------:  | -------:  | -------:  |
| Nifty         |           |           |           |
| Fusion-Moves  |           |           |           |
| Primal        | -562303.4 | -343945.4 | -521574.0 |
| Runtime       | 87.1      | 299.5     | 107.6     |
| ILP           |           |           |           |
| Primal        | -562304.5 | -343948.5 | -521576.5 |
| Runtime       | 118.6     | 349.8     | 329.6     |
| OpenGM        |           |           |           |
| Fusion-Moves  |           |           |           |
| Primal        | -560124.8 | -334269.8 | -487855.2 |
| Runtime       | 8.5       | 36.3      | 13.4      |
| ILP           |           |           |           |
| Primal        | -562304.5 | -343948.5 | -521576.5 |
| Runtime       | 1182.0    | 496.1     | 869.4     |
