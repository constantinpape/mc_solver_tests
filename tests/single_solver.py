import argparse
from functools import partial
import sys
sys.path.append('..')
from utils import run_fusion_moves_nifty, run_ilp_nifty, run_mc_mp_cmdline, run_mc_mp_pybindings, run_mp_nifty
from utils import read_from_mcppl

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("uv_path", type = str)
    parser.add_argument("cost_path", type = str)
    parser.add_argument("solver_type", type = str)
    parser.add_argument("n_threads", type = int, default = 1)
    args = parser.parse_args()

    n_var, uv_ids, costs = read_from_mcppl(args.uv_path, args.cost_path)
    solver_type = args.solver_type
    n_threads = args.n_threads
    assert solver_type in ('fm', 'mcmp_py', 'mcmp_cmd', 'ilp', 'mp_nifty')
    if solver_type == 'fm':
        solver = partial(run_fusion_moves_nifty, verbose = True)
    elif solver_type == 'ilp':
        solver = partial(run_ilp_nifty, verbose = True)
    elif solver_type == 'mcmp_py':
        solver = partial(run_mc_mp_pybindings, n_threads = n_threads)
    elif solver_type == 'mcmp_cmd':
        solver = partial(run_mc_mp_cmdline, n_threads = n_threads)
    elif solver_type == 'mp_nifty':
        solver = run_mp_nifty

    return n_var, uv_ids, costs, solver


if __name__ == '__main__':
    n_var, uv_ids, costs, solver = parse_args()
    solver(n_var, uv_ids, costs)
