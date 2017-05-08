import os
import time
import subprocess
import numpy as np

# solver libraries
import opengm
import nifty
ilp_bkend = 'cplex'

################################################
#### OpenGM Solver
################################################

def run_fusion_moves_opengm(n_var, uv_ids, costs,
        n_threads = 20,
        seed_fraction = 0.001,
        verbose = False):

    # set up the opengm model
    states = np.ones(n_var) * n_var
    gm = opengm.gm(states)

    # potts model
    potts_shape = [n_var, n_var]

    potts = opengm.pottsFunctions(potts_shape,
                                  np.zeros_like( costs ),
                                  costs )

    # potts model to opengm function
    fids_b = gm.addFunctions(potts)
    gm.addFactors(fids_b, uv_ids)

    pparam = opengm.InfParam(seedFraction = seed_fraction)
    parameter = opengm.InfParam(generator='randomizedWatershed',
                                proposalParam=pparam,
                                numStopIt = 5000,
                                numIt = 20)

    inf = opengm.inference.IntersectionBased(gm, parameter=parameter)

    t_inf = time.time()
    if verbose:
        inf.infer(inf.verboseVisitor())
    else:
        inf.infer()
    t_inf = time.time() - t_inf

    res_node = inf.arg()
    e_glob = gm.evaluate(res_node)

    return res_node, e_glob, t_inf


def run_ilp_opengm(n_var, uv_ids, costs,
        verbose = False):
    # set up the opengm model
    states = np.ones(n_var) * n_var
    gm = opengm.gm(states)

    # potts model
    potts_shape = [n_var, n_var]
    potts = opengm.pottsFunctions(potts_shape,
                                  np.zeros_like( costs ),
                                  costs )

    # potts model to opengm function
    fids_b = gm.addFunctions(potts)

    gm.addFactors(fids_b, uv_ids)

    # the workflow, we use
    wf = "(IC)(CC-IFD)"

    param = opengm.InfParam(
            workflow = wf,
            verbose = verbose,
            verboseCPLEX = verbose,
            numThreads = 4 )

    inf = opengm.inference.Multicut(gm, parameter=param)
    t_inf = time.time()
    inf.infer()
    t_inf = time.time() - t_inf
    res_node = inf.arg()
    e_glob = gm.evaluate(res_node)

    return res_node, e_glob, t_inf


################################################
#### Nifty Solver
################################################


def nifty_mc_objective(n_var, uv_ids, costs):
    g = nifty.graph.UndirectedGraph(n_var)
    g.insertEdges(uv_ids)
    assert g.numberOfEdges == uv_ids.shape[0], "%i, %i" % (g.numberOfEdges, uv_ids.shape[0])
    assert g.numberOfEdges == costs.shape[0],  "%i, %i" % (g.numberOfEdges, costs.shape[0])
    return nifty.graph.multicut.multicutObjective(g, costs)


def run_fusion_moves_nifty(n_var, uv_ids, costs,
        n_threads = 20,
        seed_fraction = 0.001,
        verbose = False,
        timeout = 0
        ):
    obj = nifty_mc_objective(n_var, uv_ids, costs)

    greedy = obj.greedyAdditiveFactory().create(obj)

    backend_factory = obj.multicutIlpFactory(ilpSolver=ilp_bkend,verbose=0,
        addThreeCyclesConstraints=True,
        addOnlyViolatedThreeCyclesConstraints=True
    )

    factory = obj.fusionMoveBasedFactory(
        verbose=1,
        fusionMove=obj.fusionMoveSettings(mcFactory=backend_factory),
        proposalGen=obj.watershedProposals(sigma=10, seedFraction=seed_fraction),
        numberOfIterations = 3000,
        numberOfParallelProposals = 2*n_threads,
        numberOfThreads = n_threads,
        stopIfNoImprovement = 20,
        fuseN=2,
    )

    solver = factory.create(obj)

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


def run_ilp_nifty(n_var, uv_ids, costs,
        verbose = False,
        timeout = 0):

    obj = nifty_mc_objective(n_var, uv_ids, costs)
    solver = obj.multicutIlpFactory(ilpSolver=ilp_bkend,verbose=0,
        addThreeCyclesConstraints=True,
        addOnlyViolatedThreeCyclesConstraints=True
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
    if with_visitor:
        ret = solver.optimize(visitor=visitor)
    else:
        ret = solver.optimize()
    t_inf = time.time() - t_inf

    mc_energy = obj.evalNodeLabels(ret)
    return ret, mc_energy, t_inf


# TODO Test this !!!
def run_kl_nifty(n_var, uv_ids, costs,
        verbose = False,
        timeout = 0):

    obj = nifty_mc_objective(n_var, uv_ids, costs)
    greedy = obj.greedyAdditiveFactory().create(obj)
    solver = obj.multicutKernighanLinFactory().create(obj)

    t_inf = time.time()
    ret = greedy.optimize()
    ret = solver.optimize(nodeLabels = ret)
    t_inf = time.time() - t_inf

    mc_energy = obj.evalNodeLabels(ret)
    return ret, mc_energy, t_inf


################################################
#### LP_MP Solver
################################################


def write_to_opengm(n_var, uv_ids, costs, out_file):
    states = np.ones(n_var) * n_var
    gm_global = opengm.gm(states)
    # potts model
    potts_shape = [n_var, n_var]
    potts = opengm.pottsFunctions(potts_shape,
                                  np.zeros_like(costs),
                                  costs)
    # potts model to opengm function
    fids_b = gm_global.addFunctions(potts)
    gm_global.addFactors(fids_b, uv_ids.astype('uint32'))

    # save the opengm model
    opengm.saveGm(gm_global, out_file)


def run_mc_mp_cmdline(n_var, uv_ids, costs,
        max_iter = 1000,
        n_threads = 1):
    write_to_opengm(n_var, uv_ids, costs, './tmp.gm')

    # TODO with or without odd_wheel ?
    home_dir = os.path.expanduser("~")
    binary_odd_wheel = os.path.join(home_dir, 'Work/software/bld/LP_MP/src/solvers/multicut/multicut_opengm_srmp_cycle_odd_wheel')
    binary           = os.path.join(home_dir, 'Work/software/bld/LP_MP/src/solvers/multicut/multicut_opengm_srmp_cycle')

    options =  [
        binary,
        '-i', './tmp.gm',
        '--tighten',
        '--standardReparametrization', 'anisotropic',
        '--tightenReparametrization', 'damped_uniform',
        '--roundingReparametrization', 'damped_uniform',
        '--tightenIteration', '2',
        '--tightenInterval', '49',
        '--tightenSlope', '0.1',
        '--tightenConstraintsPercentage', '0.05',
        '--primalComputationInterval', '13',
        '--maxIter', str(max_iter),
        '--numLpThreads', str(n_threads)
    ]


    t_inf = time.time()
    #out = subprocess.check_output(
    subprocess.call(
        options
    )
    t_inf = time.time() - t_inf

    #out = out.split('\n')
    #l_energy = out[-7].split()
    #energy = float(l_energy[-1])
    energy = -100

    os.remove('./tmp.gm')
    return np.zeros(n_var), energy, t_inf


def run_mc_mp_pybindings(n_var, uv_ids, costs,
        max_iter = 1000,
        timeout  = 0,
        n_threads= 1
    ):


    # dirty hack for lp_mp pybindings
    home_dir = os.path.expanduser("~")
    import sys
    sys.path.append( os.path.join(home_dir, 'software/bld/LP_MP/python') )
    import lp_mp

    # nifty graph and objective for node labels and energy
    g = nifty.graph.UndirectedGraph(int(n_var))
    g.insertEdges(uv_ids)
    assert g.numberOfEdges == costs.shape[0], "%i , %i" % (g.numberOfEdges, costs.shape[0])
    assert g.numberOfEdges == uv_ids.shape[0], "%i, %i" % (g.numberOfEdges, uv_ids.shape[0])
    obj = nifty.graph.multicut.multicutObjective(g, costs)

    multicut_opts = lp_mp.solvers.MulticutOptions(
            maxIter = max_iter,
            timeout = timeout,
            standardReparametrization = 'anisotropic',
            tightenReparametrization  = 'damped_uniform',
            roundingReparametrization = 'damped_uniform',
            tightenIteration          = 2,
            tightenInterval           = 49,
            tightenSlope              = 0.1,
            tightenConstraintsPercentage = 0.05,
            primalComputationInterval = 13,
            nThreads                  = n_threads
            )

    # FIXME make this compatible with numpy arrays for uv_ids too
    t_inf = time.time()
    mc_edges = lp_mp.solvers.multicut(
            [(uv[0],uv[1]) for uv in uv_ids],
            costs,
            multicut_opts
            )
    t_inf = time.time() - t_inf

    # edge labels to node labels
    merge_edges = uv_ids[np.array(mc_edges) == False]
    ufd = nifty.ufd.ufd(n_var)
    ufd.merge(merge_edges)
    mc_nodes = ufd.elementLabeling()

    mc_energy = obj.evalNodeLabels(mc_nodes)

    return mc_nodes, mc_energy, t_inf
