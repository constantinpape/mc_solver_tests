import argparse
from functools import partial
import sys
sys.path.append('..')
from utils import run_fusion_moves_nifty, run_ilp_nifty, run_mc_mp_cmdline, run_mc_mp_pybindings
from utils import read_from_mcluigi

# TODO
# TODO reasonable seed fraction default value for nifty - fm
# TODO
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("model_path", type = str)
    parser.add_argument("solver_type", type = str)
    parser.add_argument("timeout", type = int)
    args = parser.parse_args()

    n_var, uv_ids, costs = read_from_mcluigi(args.model_path)
    solver_type = args.solver_type
    assert solver_type in ('fm', 'mcmp_py', 'ilp')
    if solver_type == 'fm':
        solver = partial(run_fusion_moves_nifty, verbose = True, timeout = timeout)
    elif solver_type == 'ilp':
        solver = partial(run_ilp_nifty, verbose = True, timeout = timeout)
    elif solver_type == 'mcmp_py':
        solver = partial(run_mc_mp_pybindings, timeout = timeout)

    return n_var, uv_ids, costs, solver


if __name__ == '__main__':
    n_var, uv_ids, costs, solver = parse_args()
    solver(n_var, uv_ids, costs)
