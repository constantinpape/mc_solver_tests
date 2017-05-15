import argparse
from functools import partial
import sys
sys.path.append('..')
from utils import *

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

    obj = nifty_mc_objective(n_var, uv_ids, costs)

    kl_ws = True
    pgen_type = 'ws'

    solver_dict = {
        'greedy' : nifty_greedy_factory(obj),
        'fm-greedy' : nifty_fusion_move_factory(obj,
            backend_factory = nifty_greedy_factory(obj),
            seed_fraction = 0.05,
            pgen_type = pgen_type,
            kl_chain = kl_ws
            ),
        'fm-ilp' : nifty_fusion_move_factory(obj,
            backend_factory = nifty_ilp_factory(obj),
            pgen_type = pgen_type,
            seed_fraction = 0.005,
            kl_chain = kl_ws
           ),
        'fm-kl' : nifty_fusion_move_factory(obj,
            backend_factory = nifty_kl_factory(obj),
            pgen_type = pgen_type,
            seed_fraction = 0.01,
            kl_chain = kl_ws
            ),
        'fm-cgc' : nifty_fusion_move_factory(obj,
            backend_factory = nifty_cgc_factory(obj),
            seed_fraction = 0.01,
            pgen_type = pgen_type,
            kl_chain = kl_ws
            ),
        'ilp' : nifty_ilp_factory(obj),
        'cgc' : nifty_cgc_factory(obj, kl_chain = True),
        'kl'  : nifty_kl_factory(obj),
        'mp'  : nifty_mp_factory(
            obj,
            number_of_iterations = 100000,
            n_threads = 20,
            timeout = int(timeout)
        ),
        'mp-fmkl' : nifty_mp_factory(
            obj,
            number_of_iterations = 100000,
            n_threads = 20,
            timeout = int(timeout),
            backend_factory = nifty_fusion_move_factory(
                obj,
                n_threads = 20,
                backend_factory = nifty_kl_factory(obj),
                seed_fraction = 0.005,
                number_of_iterations = 20,
                n_stop = 4
            )
        ),
        'mp-fmgreedy' : nifty_mp_factory(
            obj,
            number_of_iterations = 100000,
            n_threads = 20,
            timeout = int(timeout),
            backend_factory = nifty_fusion_move_factory(
                obj,
                n_threads = 20,
                backend_factory = nifty_greedy_factory(obj),
                seed_fraction = 0.01,
                number_of_iterations = 25,
                n_stop = 3,
                kl_chain = True,
                n_fuse = 1,
                parallel_per_thread = 1
            )
        ),
    }

    factory = solver_dict[solver_type]
    return obj, factory


if __name__ == '__main__':
    obj, factory = parse_args()
    run_nifty_solver(obj, factory, verbose = True, time_limit = 3600)
