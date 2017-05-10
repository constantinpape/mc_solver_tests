import os
import time
import nifty
import numpy as np

from run_solvers import nifty_mc_objective

ilp_bkend = 'cplex'


# TODO more mp settings
def mp_factory(obj, mp_primal_rounder,
        max_iter = 1000,
        timeout  = 0,
        n_threads = 1,
        tighten   = True,
        standardReparametrization = 'anisotropic',
        tightenReparametrization  = 'damped_uniform',
        roundingReparametrization = 'damped_uniform',
        tightenIteration          = 2,
        tightenInterval           = 49,
        tightenSlope              = 0.1,
        tightenConstraintsPercentage = 0.05,
        primalComputationInterval = 13,
        n_threads_fuse = 1,
        seed_fraction_fuse = 0.001
        ):
    assert mp_primal_rounder in ('greedy', 'kl', 'ilp', 'fm-ilp', 'fm-mp', 'cgc'), mp_primal_rounder

    if mp_primal_rounder == 'greedy':
        backend_factory = obj.greedyAdditiveFactory()
        greedy_ws = False

    elif mp_primal_rounder == 'kl':
        backend_factory = obj.multicutAndresKernighanLinFactory()
        greedy_ws = False

    elif mp_primal_rounder == 'ilp':
        backend_factory = obj.multicutIlpFactory(
                ilpSolver=ilp_bkend,
                verbose=0,
                addThreeCyclesConstraints=True,
                addOnlyViolatedThreeCyclesConstraints=True
            )
        greedy_ws = False

    elif mp_primal_rounder == 'cgc':
        backend_factory = obj.cgcFactory()
        greedy_ws = True

    elif mp_primal_rounder in ('fm-ilp', 'fm-mp'):

        if mp_primal_rounder == 'fm-ilp':
            fm_factory = obj.multicutIlpFactory(
                    ilpSolver=ilp_bkend,
                    verbose=0,
                    addThreeCyclesConstraints=True,
                    addOnlyViolatedThreeCyclesConstraints=True
                )
        else:
            fm_factory = mp_factory(obj, 'kl', max_iter = 500)

        backend_factory = obj.fusionMoveBasedFactory(
            verbose=0,
            fusionMove=obj.fusionMoveSettings(mcFactory=fm_factory),
            proposalGen=obj.watershedProposals(sigma=10, seedFraction=seed_fraction_fuse),
            numberOfIterations = 1000,
            numberOfParallelProposals = 2*n_threads_fuse,
            numberOfThreads = n_threads_fuse,
            stopIfNoImprovement = 8,
            fuseN=2,
        )
        greedy_ws = True

    factory = obj.multicutMpFactory(
            mcFactory = backend_factory,
            greedyWarmstart = greedy_ws,
            timeout = timeout,
            numberOfIterations = max_iter,
            numberOfThreads            = n_threads,
            tighten                    = tighten,
            standardReparametrization  = standardReparametrization,
            tightenReparametrization   = tightenReparametrization,
            roundingReparametrization  = roundingReparametrization,
            tightenIteration           = tightenIteration,
            tightenInterval            = tightenInterval,
            tightenSlope               = tightenSlope,
            tightenConstraintsPercentage= tightenConstraintsPercentage,
            primalComputationInterval   = primalComputationInterval
    )
    return factory


def run_mp_nifty(n_var, uv_ids, costs,
        mp_primal_rounder = 'kl',
        max_iter = 1000,
        timeout = 0,
        n_threads = 1,
        tighten   = True,
        standardReparametrization = 'anisotropic',
        tightenReparametrization  = 'damped_uniform',
        roundingReparametrization = 'damped_uniform',
        tightenIteration          = 2,
        tightenInterval           = 49,
        tightenSlope              = 0.1,
        tightenConstraintsPercentage = 0.05,
        primalComputationInterval = 13
        ):

    obj = nifty_mc_objective(n_var, uv_ids, costs)

    solver = mp_factory(obj, mp_primal_rounder,
            max_iter                   = max_iter,
            timeout                    = timeout,
            n_threads                  = n_threads,
            tighten                    = tighten,
            standardReparametrization  = standardReparametrization,
            tightenReparametrization   = tightenReparametrization,
            roundingReparametrization  = roundingReparametrization,
            tightenIteration           = tightenIteration,
            tightenInterval            = tightenInterval,
            tightenSlope               = tightenSlope,
            tightenConstraintsPercentage= tightenConstraintsPercentage,
            primalComputationInterval   = primalComputationInterval
        ).create(obj)

    t_inf = time.time()
    ret = solver.optimize()
    t_inf = time.time() - t_inf

    mc_energy = obj.evalNodeLabels(ret)
    return ret, mc_energy, t_inf


def run_fusion_moves_mp(n_var, uv_ids, costs,
        n_threads = 20,
        seed_fraction = 0.001,
        verbose = False,
        timeout = 0,
        mp_primal_rounder = 'kl'
        ):

    obj = nifty_mc_objective(n_var, uv_ids, costs)
    greedy = obj.greedyAdditiveFactory().create(obj)
    backend_factory = mp_factory(obj, mp_primal_rounder, max_iter = 200)

    solver = obj.fusionMoveBasedFactory(
        verbose=1,
        fusionMove=obj.fusionMoveSettings(mcFactory=backend_factory),
        proposalGen=obj.watershedProposals(sigma=10, seedFraction=seed_fraction),
        numberOfIterations = 3000,
        numberOfParallelProposals = 2*n_threads,
        numberOfThreads = n_threads,
        stopIfNoImprovement = 20,
        fuseN=2,
    ).create(obj)

    with_visitor = False
    if verbose or timeout > 0:
        with_visitor = True
        if verbose and timeout > 0:
            visitor = obj.multicutVerboseVisitor(1, timeout)
        elif not verbose:
            visitor = obj.multicutVerboseVisitor(1000000, timeout)
        else:
            visitor = obj.multicutVerboseVisitor(1)

    t_inf = time.time()
    ret    = greedy.optimize()
    if with_visitor:
        ret = solver.optimize(nodeLabels=ret,visitor=visitor)
    else:
        ret = solver.optimize(nodeLabels=ret)
    t_inf = time.time() - t_inf
    mc_energy = obj.evalNodeLabels(ret)

    return ret, mc_energy, t_inf
