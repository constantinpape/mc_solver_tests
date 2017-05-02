import argparse
from functools import partial
import sys
sys.path.append('..')
from utils import run_fusion_moves_nifty, run_ilp_nifty, run_mc_mp_cmdline, run_mc_mp_pybindings, run_mp_nifty
from utils import read_from_mcppl

def parse_args():
    print "Parsing"
    parser = argparse.ArgumentParser()
    parser.add_argument("uv_path", type = str)
    parser.add_argument("cost_path", type = str)
    parser.add_argument("solver_type", type = str)
    args = parser.parse_args()
    print "Parsing"

    n_var, uv_ids, costs = read_from_mcppl(args.uv_path, args.cost_path)
    solver_type = args.solver_type
    assert solver_type in ('fm', 'mcmp_py', 'mcmp_cmd', 'ilp', 'mp_nifty')
    if solver_type == 'fm':
        solver = partial(run_fusion_moves_nifty, verbose = True)
    elif solver_type == 'ilp':
        solver = partial(run_ilp_nifty, verbose = True)
    elif solver_type == 'mcmp_py':
        solver = run_mc_mp_pybindings
    elif solver_type == 'mcmp_cmd':
        solver = run_mc_mp_cmdline
    elif solver_type == 'mp_nifty':
        solver = run_mp_nifty

    return n_var, uv_ids, costs, solver


if __name__ == '__main__':
    n_var, uv_ids, costs, solver = parse_args()
    solver(n_var, uv_ids, costs)
