import cPickle as pickle
import numpy as np


def parse_out_niftyfm(out_path, with_iter = False):

    with open(out_path) as f:
        out = f.read()
    out = out.split('\n')

    energies  = []
    run_times = []
    iter_without_improvement = []

    for line in out:
        if not line.startswith('Energy:'):
            if line.startswith('end inference'):
                break
            else:
                continue
        values = line.split()
        energies.append(float(values[1]))
        run_times.append(int(values[3]))
        iter_without_improvement.append( int(float(values[5])) )

    if with_iter:
        return run_times, energies, iter_without_improvement
    else:
        return run_times, energies


def parse_out_niftyilp(out_path, with_n_violated = False):

    with open(out_path) as f:
        out = f.read()
    out = out.split('\n')

    energies  = []
    run_times = []
    n_violated = []

    for line in out[1:]:
        if not line.startswith('Energy:'):
            if line.startswith('end inference'):
                break
            else:
                continue
        values = line.split()
        energies.append(float(values[1]))
        run_times.append(int(values[3]))
        n_violated.append( int(float(values[5])) )

    if with_n_violated:
        return run_times, energies, n_violated
    else:
        return run_times, energies


def parse_out_mcmp(out_path, return_dual = False):

    with open(out_path) as f:
        out = f.read()
    out = out.split('\n')

    primal    = []
    dual      = []
    rt_primal = []
    rt_dual   = []
    dual_improvements = []

    for ii, line in enumerate(out):

        assert isinstance(line, str), line

        if line.startswith('best triplet'):
            line = line.split()
            dual_improvements.append(line[-1])
            continue

        if not line.startswith('iteration'):
            continue

        line = line.split()
        iter_num    = int(line[2][:-1])
        lower_bound = float(line[6][:-1])
        run_time   = float(line[-1][:-1])

        rt_dual.append(run_time)
        dual.append(lower_bound)

        if line[7] == 'upper':
            val = line[10][:-1] if not line[10] == 'inf,' else '0'
            primal.append(
                float( val )
            )
            rt_primal.append(run_time)

    # postprocess the primals for a better plot and drop primals that have 0 value
    primal = np.array(primal)
    rt_primal = np.array(rt_primal)
    mask = primal != 0
    primal = primal[mask]
    rt_primal = rt_primal[mask]

    if return_dual:
        return rt_primal, primal, rt_dual, dual, dual_improvements
    else:
        return rt_primal, primal
