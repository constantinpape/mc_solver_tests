import subprocess
import vigra
import os
import re
import cPickle as pickle
import numpy as np

import sys
sys.path.append('..')
from utils import model_paths_mcluigi


def save_cmdline_output(out, save_file):
    with open(save_file,'w') as f:
        f.write(out)


def anytime_data_small_samples():

    def _run(sample, solver_type, n_threads = 1):
        assert solver_type in ('fm', 'mcmp_py', 'mcmp_cmd', 'ilp', 'mp_nifty')
        uv_path, cost_path = model_paths_new[sample]
        #subprocess.call(
        out = subprocess.check_output(
                ['python', 'single_solver.py', uv_path, cost_path, solver_type, str(n_threads)])
        return out

    save_folder = './anytime_data'
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    #samples = ('sampleA', 'sampleB', 'sampleC')
    samples = ('sampleB','sampleC')

    for sample in samples:
        print sample
        #for solver in ('ilp', 'fm', 'mcmp_py'):
        for solver in ('mcmp_py', 'mcmp_cmd'):
            print solver
            for n_threads in (1,2,4,8,20):
                print n_threads
                out = _run(sample, solver, n_threads)
                save_cmdline_output(out, save_folder + '/%s_%s_%i_threads.txt'% (sample, solver, n_threads))


def anytime_data_sampleD():

    # 2 hours default timeout
    def _run(sample, solver_type, timeout = 3600, n_threads = 20):
        assert solver_type in ('fm', 'mcmp', 'mcmp_cmd', 'ilp', 'mcmp-fmkl')
        model_path = model_paths_mcluigi[sample]
        out = subprocess.check_output(
                ['python', 'single_solver_sampleD.py', model_path, solver_type, str(timeout), str(n_threads)])
        return out

    save_folder = './anytime_data/sampleD'
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    samples = ('sampleD_medium',)# 'sampleD_large')
    for sample in samples:
        print sample
        for solver in ('mcmp-fmkl', 'fm', 'mcmp'):
            print solver
            out = _run(sample, solver)
            save_cmdline_output(out, save_folder + '/%s_%s.txt'% (sample, solver))


if __name__ == '__main__':
    anytime_data_sampleD()
    #anytime_data_small_samples()
