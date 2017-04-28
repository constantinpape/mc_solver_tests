# Multicut Solver Tests

Compare different multicut solver:
* Opengm Ilp-Solver and Fusion-Moves solver
* Nifty Ilp-Solver and Fusion-Moves solver
* LP_MP Multicut solver

## Opengm vs nifty

On cremi problems from training samples:

| Primal Energy | Sample A  | Sample B  | Sample C  |
|-------------  | -------:  | -------:  | -------:  |
| Nifty         |           |           |           |
| Fusion-Moves  | -562303.4 | -343945.4 | -521574.0 |
| ILP           | -562304.5 | -343948.5 | -521576.5 |
| OpenGM        |           |           |           |
| Fusion-Moves  | -560124.8 | -334269.8 | -487855.2 |
| ILP           | -562304.5 | -343948.5 | -521576.5 |

| Runtime [s]   | Sample A  | Sample B  | Sample C  |
|-------------  | -------:  | -------:  | -------:  |
| Nifty         |           |           |           |
| Fusion-Moves  | 87.1      | 299.5     | 107.6     |
| ILP           | 118.6     | 349.8     | 329.6     |
| OpenGM        |           |           |           |
| Fusion-Moves  | 8.5       | 36.3      | 13.4      |
| ILP           | 1182.0    | 496.1     | 869.4     |
