import argparse
from functools import partial
import sys
sys.path.append('..')
from utils import run_fusion_moves_nifty, run_mc_mp_pybindings
from utils import read_from_mcppl

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("uv_path", type = str)
    parser.add_argument("cost_path", type = str)
    parser.add_argument("solver_type", type = str)
    args = parser.parse_args()

    n_var, uv_ids, costs = read_from_mcppl(args.uv_path, args.cost_path)
    solver_type = args.solver_type
    assert solver_type in ('fm', 'mcmp')
    solver = run_mc_mp_pybindings if solver_type == 'mcmp' else partial(run_fusion_moves_nifty, verbose = True)
    return n_var, uv_ids, costs, solver


if __name__ == '__main__':
    n_var, uv_ids, costs, solver = parse_args()
    solver(n_var, uv_ids, costs)
