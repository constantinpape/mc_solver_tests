import cPickle as pickle
import os

import sys
sys.path.append('..')

#
from utils import run_nifty_solver_with_logger, nifty_mc_objective, run_nifty_solver

# TODO import all existing and add more !
# import all releveant nifty solver factories
from utils import nifty_fusion_move_factory, nifty_kl_factory, nifty_ilp_factory

from utils import read_from_mcluigi
from utils import model_paths_bmc


def run_exp(sample, padded):
    sample_str = 'sample_%s_%s' % (sample, 'padded' if padded else 'small')
    print "Running experiments for %s" % sample_str

    model_path = model_paths_bmc[sample_str]
    mc_obj = nifty_mc_objective(*read_from_mcluigi(model_path))

    # TODO nifty fm-cc solver
    solvers = {
        'kl': nifty_kl_factory(mc_obj, use_andres=False),
        'fm_kl': nifty_fusion_move_factory(
            mc_obj,
            nifty_kl_factory(mc_obj, use_andres=False),
            n_threads=8
        ),
        'fm_ilp': nifty_fusion_move_factory(
            mc_obj,
            nifty_ilp_factory(mc_obj),
            n_threads=8
        ),
        'ilp': nifty_ilp_factory(mc_obj)
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


def compare_kl_impls(sample, padded):
    sample_str = 'sample_%s_%s' % (sample, 'padded' if padded else 'small')
    model_path = model_paths_bmc[sample_str]
    mc_obj = nifty_mc_objective(*read_from_mcluigi(model_path))

    _, e_nifty, t_nifty = run_nifty_solver(mc_obj, nifty_kl_factory(mc_obj, use_andres=False))
    _, e_andres, t_andres = run_nifty_solver(mc_obj, nifty_kl_factory(mc_obj, use_andres=True))

    print "Inference with nifty kl in %f s with energy %f." % (e_nifty, t_nifty)
    print "Inference with andres kl in %f s with energy %f." % (e_andres, t_andres)


if __name__ == '__main__':
    sample = 'A'
    padded = False
    run_exp(sample, padded)
    # compare_kl_impls(sample, padded)
