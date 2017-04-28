# Multicut Solver Tests

Compare different multicut solver:
* Opengm Ilp-Solver and Fusion-Moves solver
* Nifty Ilp-Solver and Fusion-Moves solver
* LP_MP Multicut solver

## Small Cremi Problems

Nifty Fusionmoves run with 20 Threads.
LP_MP run with 2500 max iterations and for all three models
the solver terminated because it exceeded this max iteration.

| Primal Energy | Sample A  | Sample B  | Sample C  |
|-------------  | -------:  | -------:  | -------:  |
| Nifty         |           |           |           |
| Fusion-Moves  | -562303.4 | -343945.4 | -521574.0 |
| ILP           | -562304.5 | -343948.5 | -521576.5 |
| OpenGM        |           |           |           |
| Fusion-Moves  | -560124.8 | -334269.8 | -487855.2 |
| ILP           | -562304.5 | -343948.5 | -521576.5 |
| LP_MP         |           |           |           |
|               | -562302.2 | -343943.5 | -521569.4 |

| Runtime [s]   | Sample A  | Sample B  | Sample C  |
|-------------  | -------:  | -------:  | -------:  |
| Nifty         |           |           |           |
| Fusion-Moves  | 87.1      | 299.5     | 107.6     |
| ILP           | 118.6     | 349.8     | 329.6     |
| OpenGM        |           |           |           |
| Fusion-Moves  | 8.5       | 36.3      | 13.4      |
| ILP           | 1182.0    | 496.1     | 869.4     |
| LP_MP         |           |           |           |
|               | 475.4     | 681.3     | 635.3     |
