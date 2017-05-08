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


## Message Passing Multicut

### Test Parallel

Runtimes:

| N-Threads  | SampleA | SampleB | SampleC |
| ---------: | ------: | ------: | ------: |
| 1          | 249.5   | 273.2   | 332.3   |
| 2          | 185.2   | 232.8   | 260.6   |
| 4          | 113.3   | 152.4   | 202.6   |
| 8          | 83.9    | 94.6    | 136.0   |
| 20         | 63.1    | 71.6    | 94.6    |

Primal Energies:

| N-Threads  | SampleA | SampleB | SampleC |
| ---------: | ------: | ------: | ------: |
| 1          | -562303 | -343945 | -521572 |
| 2          | -562303 | -343945 | -521572 |
| 4          | -562300 | -343944 | -521571 |
| 8          | -562303 | -343944 | -521569 |
| 20         | -562303 | -343944 | -521570 |
