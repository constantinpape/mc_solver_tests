import cPickle as pickle
import os

import sys
sys.path.append('..')

#
from utils import run_nifty_solver_with_logger, nifty_mc_objective

# TODO import all existing and add more !
# import all releveant nifty solver factories
from utils import nifty_fusion_move_factory, nifty_kl_factory

from utils import read_from_mcluigi
from utils import model_paths_bmc


def run_exp(sample, padded):
    sample_str = 'sample_%s_%s' % (sample, 'padded' if padded else 'small')
    print "Running experiments for %s" % sample_str

    model_path = model_paths_bmc[sample_str]
    mc_obj = nifty_mc_objective(*read_from_mcluigi(model_path))

    # TODO
    solvers = {
        'kl': nifty_kl_factory(mc_obj),
        # 'fm_kl': None,
        # 'fm_ilp': None,
        # 'ilp': None
    }

    # time limit of 1 hour
    t_lim = 3600

    solver_results = {}
    for solver in solvers.keys():
        print "Running solver %s" % solver
        solver_factory = solvers[solver]
        runtimes, energies = run_nifty_solver_with_logger(mc_obj, solver_factory, 1, t_lim)
        assert len(runtimes) == len(energies)
        solver_results[solver] = {'runtimes': runtimes, 'energies': energies}

    # serialize the results
    save_folder = './new_nifty_results'
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    save_name = '%s_%s.pkl' % (
        sample_str,
        '_'.join(solvers.keys())
    )

    save_path = os.path.join(save_folder, save_name)
    with open(save_path, 'w') as f:
        pickle.dump(solver_results, f)


if __name__ == '__main__':
    sample = 'A'
    padded = False
    run_exp(sample, padded)
