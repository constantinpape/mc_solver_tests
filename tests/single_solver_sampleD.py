import argparse
from functools import partial
import sys
sys.path.append('..')
from utils import run_fusion_moves_nifty, run_ilp_nifty, run_mc_mp_cmdline, run_mp_nifty
from utils import read_from_mcluigi

# TODO
# TODO reasonable seed fraction default value for nifty - fm
# TODO
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("model_path", type = str)
    parser.add_argument("solver_type", type = str)
    parser.add_argument("timeout", type = int)
    parser.add_argument("n_threads", type = int)
    args = parser.parse_args()

    n_var, uv_ids, costs = read_from_mcluigi(args.model_path)
    solver_type = args.solver_type
    timeout     = args.timeout
    n_threads   = args.n_threads
    assert solver_type in ('fm', 'mcmp', 'ilp', 'mcmp-fmkl')
    if solver_type == 'fm':
        solver = partial(run_fusion_moves_nifty, verbose = True, timeout = timeout, seed_fraction = 1e-5, n_threads = n_threads)
    elif solver_type == 'ilp':
        solver = partial(run_ilp_nifty, verbose = True, timeout = timeout)
    elif solver_type == 'mcmp':
        solver = partial(run_mp_nifty, timeout = timeout, max_iter = long(1e8), n_threads = n_threads)
    elif solver_type == 'mcmp-fmkl':
        solver = partial(run_mp_nifty, timeout = timeout, max_iter = long(1e8), n_threads = n_threads, n_threads_fuse = 20, mp_primal_rounder = 'fm-kl')

    return n_var, uv_ids, costs, solver


if __name__ == '__main__':
    n_var, uv_ids, costs, solver = parse_args()
    solver(n_var, uv_ids, costs)
