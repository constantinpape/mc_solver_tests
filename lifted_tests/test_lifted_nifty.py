import numpy as np
from functools import partial

import sys
sys.path.append('..')
from utils import *


def test_lifted(model, solver_choice):

    obj = read_lifted(model_paths_lifted[model])
    solver_dict = {
            'greedy' : partial(
                run_nifty_lmc,
                obj,
                greedy_lmc_factory(obj),
                visit_nth = 500
                ),
            'kl' : partial(
                run_nifty_lmc,
                obj,
                kl_lmc_factory(obj),
                greedy_ws = True,
                visit_nth = 50
                ),
            'fm-kl' : partial(
                run_nifty_lmc,
                obj,
                fusion_move_lmc_factory(obj),
                greedy_ws = True,
                kl_ws     = True,
                visit_nth = 1
                ),
            'mp' : partial(
                run_nifty_lmc,
                obj,
                mp_lmc_factory(obj)
                )
    }

    res_dict = {}
    for solver_name in solver_choice:
        solver = solver_dict[solver_name]
        _, e, t = solver()
        res_dict[solver_name] = (e,t)

    return res_dict



def test_isbi():
    model = 'isbi'
    solver_choice = ['greedy','kl','fm-kl']#,'mp']
    res_dict = test_lifted(model, solver_choice)

    print "Results Summary for LMC on ISBI"
    for solver in solver_choice:
        res = res_dict[solver]
        print solver
        print "Energy : %f" % res[0]
        print "Runtime: %f s" % res[1]


def test_snemi():
    model = 'snemi'
    solver_choice = ['greedy','kl']#,'fm-kl','mp']
    res_dict = test_lifted(model, solver_choice)

    print "Results Summary for LMC on SNEMI"
    for solver in solver_choice:
        res = res_dict[solver]
        print solver
        print "Energy : %f" % res[0]
        print "Runtime: %f s" % res[1]


if __name__ == '__main__':
    test_isbi()
    #test_snemi()
