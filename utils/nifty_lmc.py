import os
import time
import numpy as np

import nifty
import nifty.graph.optimization.lifted_multicut as nifty_lmc


def run_nifty_lmc(obj, factory,
        greedy_ws = False,
        kl_ws = False,
        visit_nth = 0
        ):
    solver = factory.create(obj)

    ws = False
    if greedy_ws:
        greedy = greedy_lmc_factory(obj).create(obj)
        node_res = greedy.optimize()
        ws = True

    if kl_ws:
        kl = kl_lmc_factory(obj).create(obj)
        if ws:
            node_res = kl.optimize(node_res)
        else:
            node_res = kl.optimize()
            ws = True

    if visit_nth:
        visitor = obj.verboseVisitor(visit_nth)

    t_inf = time.time()
    if ws and visit_nth:
        node_res = solver.optimize(visitor, node_res)
    elif ws:
        node_res = solver.optimize(node_res)
    elif visit_nth:
        node_res = solver.optimize(visitor)
    else:
        node_res = solver.optimize()
    t_inf = time.time() - t_inf

    energy = obj.evalNodeLabels(node_res)

    return node_res, energy, t_inf


# TODO chaining in nifty lmcs ?!
def kl_lmc_factory(obj, use_andres = False):
    return obj.liftedMulticutKernighanLinFactory()

# TODO andres factory
def greedy_lmc_factory(obj, use_andres = False):
    if use_andres:
        return None # TODO
    else:
        return obj.liftedMulticutGreedyAdditiveFactory()

def fusion_move_lmc_factory(obj,
        seed_fraction = 0.1):
    pgen = obj.watershedProposalGenerator(
            seedingStrategie = 'SEED_FROM_LOCAL',
            sigma = 1,
            numberOfSeeds = seed_fraction
            )
    return obj.fusionMoveBasedFactory( # we leave the number of iterations at default values for now
            proposalGenerator = pgen,
            #numberOfThreads = ExperimentSettings().n_threads
            numberOfThreads = 1 # TODO only n = 1 implemented
            )

# TODO params
def mp_lmc_factory(obj):
    return obj.liftedMulticutMpFactory()
