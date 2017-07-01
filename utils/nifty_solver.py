import time
import nifty
import nifty.graph.optimization.multicut as nifty_mc
ilp_bkend = 'cplex'


def nifty_mc_objective(n_var, uv_ids, costs):
    g = nifty.graph.UndirectedGraph(n_var)
    g.insertEdges(uv_ids)
    assert g.numberOfEdges == uv_ids.shape[0], "%i, %i" % (g.numberOfEdges, uv_ids.shape[0])
    assert g.numberOfEdges == costs.shape[0], "%i, %i" % (g.numberOfEdges, costs.shape[0])
    return nifty_mc.multicutObjective(g, costs)


def run_nifty_solver(
        obj,
        factory,
        verbose=False,
        time_limit=None
):

    solver = factory.create(obj)
    with_visitor = False
    if verbose or time_limit is not None:
        with_visitor = True
        visit_nth = 1 if verbose else int(1000000000)
        # print "visiting every %i with tlim %i" % (visit_nth, time_limit)
        visitor = obj.multicutVerboseVisitor(visit_nth, time_limit)

    t_inf = time.time()
    if with_visitor:
        ret = solver.optimize(visitor)
    else:
        ret = solver.optimize()
    t_inf = time.time() - t_inf
    mc_energy = obj.evalNodeLabels(ret)
    return ret, mc_energy, t_inf


def nifty_greedy_factory(
        obj,
        use_andres=False
):
    if use_andres:
        return obj.greedyAdditiveFactory()
    else:
        return obj.multicutAndresGreedyAdditiveFactory()


def nifty_fusion_move_factory(
        obj,
        backend_factory,
        n_threads=20,
        seed_fraction=0.001,
        greedy_chain=True,
        kl_chain=False,
        number_of_iterations=2000,
        n_stop=20,
        pgen_type='ws',
        parallel_per_thread=2,
        n_fuse=2
):

    assert pgen_type in ('ws', 'greedy')
    if pgen_type == 'ws':
        pgen = obj.watershedProposals(sigma=10, seedFraction=seed_fraction)
    else:
        pgen = obj.greedyAdditiveProposals(sigma=10)

    fm_factory = obj.fusionMoveBasedFactory(
        fusionMove=obj.fusionMoveSettings(mcFactory=backend_factory),
        proposalGen=pgen,
        numberOfIterations=number_of_iterations,
        numberOfParallelProposals=parallel_per_thread * n_threads,
        numberOfThreads=n_threads,
        stopIfNoImprovement=n_stop,
        fuseN=n_fuse
    )

    if kl_chain and greedy_chain:
        # print "Kl + Greedy Chain"
        kl_factory = nifty_kl_factory(obj, True)
        return obj.chainedSolversFactory([kl_factory, fm_factory])
    elif kl_chain and not greedy_chain:
        # print "Kl Chain"
        kl_factory = nifty_kl_factory(obj, False)
        return obj.chainedSolversFactory([kl_factory, fm_factory])
    elif greedy_chain and not kl_chain:
        # print "Greedy Chain"
        greedy = nifty_greedy_factory(obj)  # andres = True
        return obj.chainedSolversFactory([greedy, fm_factory])
    else:
        return fm_factory


def nifty_ilp_factory(
        obj
):
    factory = obj.multicutIlpFactory(
        ilpSolver=ilp_bkend,
        addThreeCyclesConstraints=True,
        addOnlyViolatedThreeCyclesConstraints=True
    )
    return factory


# TODO
def nifty_decomposer_factory(
        obj,
        backend_factory
):
    pass


def nifty_cgc_factory(
        obj,
        greedy_chain=True,
        kl_chain =False,
        cut_phase=False
):
    factory = obj.cgcFactory(doCutPhase=cut_phase)
    if kl_chain and greedy_chain:
        # print "Kl + Greedy Chain"
        kl_factory = nifty_kl_factory(obj, True)
        return obj.chainedSolversFactory([kl_factory, factory])
    elif kl_chain and not greedy_chain:
        # print "Kl Chain"
        kl_factory = nifty_kl_factory(obj, False)
        return obj.chainedSolversFactory([kl_factory, factory])
    elif greedy_chain and not kl_chain:
        # print "Greedy Chain"
        greedy = nifty_greedy_factory(obj)  # andres = True
        return obj.chainedSolversFactory([greedy, factory])
    else:
        return factory


def nifty_kl_factory(
        obj,
        greedy_chain=True
):
    return obj.multicutAndresKernighanLinFactory(greedyWarmstart=greedy_chain)


# TODO more mp settings
def nifty_mp_factory(
        obj,
        backend_factory=None,  # default is none which uses KL
        number_of_iterations=1000,
        timeout=0,
        n_threads=1,
        tighten=True,
        standardReparametrization = 'anisotropic',
        tightenReparametrization  = 'damped_uniform',
        roundingReparametrization = 'damped_uniform',
        tightenIteration          = 2,
        tightenInterval           = 49,
        tightenSlope              = 0.1,
        tightenConstraintsPercentage = 0.05,
        primalComputationInterval = 13,
):

    factory = obj.multicutMpFactory(
            mcFactory = backend_factory,
            timeout = timeout,
            numberOfIterations         =number_of_iterations,
            numberOfThreads            =n_threads,
            tighten                    =tighten,
            standardReparametrization  =standardReparametrization,
            tightenReparametrization   =tightenReparametrization,
            roundingReparametrization  =roundingReparametrization,
            tightenIteration           =tightenIteration,
            tightenInterval            =tightenInterval,
            tightenSlope               =tightenSlope,
            tightenConstraintsPercentage=tightenConstraintsPercentage,
            primalComputationInterval   =primalComputationInterval
    )
    return factory
