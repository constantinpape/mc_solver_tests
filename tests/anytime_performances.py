import subprocess
import vigra
import os
import re
import cPickle as pickle
import numpy as np
from model_paths import model_paths_new

def parse_and_save_out_niftyfm(out, save_path):
    out = out.split('\n')

    energies  = []
    run_times = []
    iter_without_improvement = []

    for line in out[1:]:
        if not line.startswith('Energy:'):
            if line.startswith('end inference'):
                break
            else:
                raise RuntimeError("Invalid line: %s" % line)
        values = line.split()
        energies.append(float(values[1]))
        run_times.append(int(values[3]))
        iter_without_improvement.append( int(float(values[5])) )

    vigra.writeHDF5(energies ,save_path, 'energies')
    vigra.writeHDF5(run_times ,save_path, 'run_times')
    vigra.writeHDF5(iter_without_improvement ,save_path, 'iter_without_improvement')


def parse_and_save_out_niftyilp(out, save_path):
    out = out.split('\n')

    energies  = []
    run_times = []
    n_violated = []

    for line in out[1:]:
        if not line.startswith('Energy:'):
            if line.startswith('end inference'):
                break
            else:
                raise RuntimeError("Invalid line: %s" % line)
        values = line.split()
        energies.append(float(values[1]))
        run_times.append(int(values[3]))
        n_violated.append( int(float(values[5])) )

    vigra.writeHDF5(energies ,save_path, 'energies')
    vigra.writeHDF5(run_times ,save_path, 'run_times')
    vigra.writeHDF5(n_violated ,save_path, 'n_violated')


def parse_and_save_out_mcmp(out, save_path):
    out = out.split('\n')

    # TODO also scrape the dual gaps etc
    primal    = []
    dual      = []
    rt_primal = []
    rt_dual   = []
    for line in out:
        if not line.startswith('iteration'):
            continue
        line = line.split()
        iter_num    = int(''.join(c for c in line[2] if c.isdigit()))
        lower_bound = float(''.join(c for c in line[6] if c.isdigit() or c == '-'))
        run_time   = float(''.join(c for c in line[-1] if c.isdigit() or c == '.'))

        rt_dual.append(run_time)
        dual.append(lower_bound)

        if line[7] == 'upper':
            val = line[10] if not line[10] == 'inf,' else '0'
            primal.append(
                float(''.join(c for c in val if c.isdigit() or c == '-'))
            )
            rt_primal.append(run_time)

    # postprocess the primals for a better plot and drop primals that have 0 value
    primal = np.array(primal)
    rt_primal = np.array(rt_primal)
    mask = primal != 0
    primal = primal[mask]
    rt_primal = rt_primal[mask]

    vigra.writeHDF5(rt_primal, save_path, 'rt_primal')
    vigra.writeHDF5(primal, save_path, 'primal')
    vigra.writeHDF5(rt_dual, save_path, 'rt_dual')
    vigra.writeHDF5(dual, save_path, 'dual')


def anytime_data():

    def _run(sample, solver_type):
        assert solver_type in ('fm', 'mcmp_py', 'mcmp_cmd', 'ilp')
        uv_path, cost_path = model_paths_new[sample]
        out = subprocess.check_output(
                ['python', 'single_solver.py', uv_path, cost_path, solver_type])
        return out

    save_folder = './anytime_data'
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    for sample in ('sampleA', 'sampleB', 'sampleC'):
        for solver in ('fm', 'mcmp_py', 'mcmp_cmd', 'ilp'):
            out = _run(sample, solver)
            if solver == 'fm':
                parse_and_save_out_niftyfm(out, save_folder + '/%s_%s.h5' % (sample, solver))
            elif solver == 'ilp':
                parse_and_save_out_niftyilp(out, save_folder + '/%s_%s.h5' % (sample, solver))
            else:
                parse_and_save_out_mcmp(out, save_folder + '/%s_%s.h5' % (sample, solver))


if __name__ == '__main__':
    anytime_data()
