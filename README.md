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


## Message Passing Multicut Checks

Summary for sampleA:
Message passing multicut:
Nifty mp     : primal: -562302.902895, t-inf: 151.826847
Pybindings mp: primal: -562299.604179, t-inf: 142.990735
Commandline  : primal: -562302.000000, t-inf: 118.498215

Summary for sampleB:
Message passing multicut:
Nifty mp     : primal: -343938.566390, t-inf: 195.830928
Pybindings mp: primal: -343938.234899, t-inf: 184.470509
Commandline  : primal: -343942.000000, t-inf: 148.182636

Summary for sampleC:
Message passing multicut:
Nifty mp     : primal: -521561.528984, t-inf: 191.396598
Pybindings mp: primal: -521567.047119, t-inf: 190.894397
Commandline  : primal: -521569.000000, t-inf: 148.263712

-> Commandline faster, possibly due to not using odd-wheel ?
+ we have some overhead in nifty due to ufd, but this should be negligable

-> this is after changing nifty to not using odd-wheel, investigate further!

Summary for sampleA:
Message passing multicut:
Nifty mp     : primal: -562302.954578, t-inf: 143.764840
Pybindings mp: primal: -562299.604179, t-inf: 141.825094
Commandline  : primal: -562302.000000, t-inf: 109.215390


Summary for sampleB:
Message passing multicut:
Nifty mp     : primal: -343937.595803, t-inf: 174.558420
Pybindings mp: primal: -343938.234899, t-inf: 180.051496
Commandline  : primal: -343942.000000, t-inf: 143.378908


Summary for sampleC:
Message passing multicut:
Nifty mp     : primal: -521566.089743, t-inf: 197.413129
Pybindings mp: primal: -521567.047119, t-inf: 179.699172
Commandline  : primal: -521569.000000, t-inf: 149.069549

TODO make sure that all parameters agree for the three solvers and then rerun exps
