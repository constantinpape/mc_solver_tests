import os
import time
import subprocess
import numpy as np

# solver libraries
import opengm
import nifty
ilp_bkend = 'cplex'


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
                                numStopIt = 3000,
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


# TODO get lower bound
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


def run_fusion_moves_nifty(n_var, uv_ids, costs,
        n_threads = 20,
        seed_fraction = 0.001,
        verbose = False
        ):

    g = nifty.graph.UndirectedGraph(n_var)
    g.insertEdges(uv_ids)
    assert g.numberOfEdges == uv_ids.shape[0], "%i, %i" % (g.numberOfEdges, uv_ids.shape[0])
    assert g.numberOfEdges == costs.shape[0],  "%i, %i" % (g.numberOfEdges, costs.shape[0])

    obj = nifty.graph.multicut.multicutObjective(g, costs)

    greedy = obj.greedyAdditiveFactory().create(obj)
    ret    = greedy.optimize()

    t_inf = time.time()

    ilpFac = obj.multicutIlpFactory(ilpSolver=ilp_bkend,verbose=0,
        addThreeCyclesConstraints=True,
        addOnlyViolatedThreeCyclesConstraints=True
    )

    factory = obj.fusionMoveBasedFactory(
        verbose=1,
        fusionMove=obj.fusionMoveSettings(mcFactory=ilpFac),
        proposalGen=obj.watershedProposals(sigma=10, seedFraction=seed_fraction),
        numberOfIterations = 3000,
        numberOfParallelProposals = 2*n_threads,
        numberOfThreads = n_threads,
        stopIfNoImprovement = 20,
        fuseN=2,
    )

    solver = factory.create(obj)

    if verbose:
        visitor = obj.multicutVerboseVisitor(1)
        ret = solver.optimize(nodeLabels=ret,visitor=visitor)
    else:
        ret = solver.optimize(nodeLabels=ret)
    t_inf = time.time() - t_inf
    mc_energy = obj.evalNodeLabels(ret)
    return ret, mc_energy, t_inf


def run_ilp_nifty(n_var, uv_ids, costs,
        verbose = False):

    g = nifty.graph.UndirectedGraph(int(n_var))
    g.insertEdges(uv_ids)
    assert g.numberOfEdges == costs.shape[0], "%i , %i" % (g.numberOfEdges, costs.shape[0])
    assert g.numberOfEdges == uv_ids.shape[0], "%i, %i" % (g.numberOfEdges, uv_ids.shape[0])
    obj = nifty.graph.multicut.multicutObjective(g, costs)

    t_inf = time.time()

    solver = obj.multicutIlpFactory(ilpSolver=ilp_bkend,verbose=0,
        addThreeCyclesConstraints=True,
        addOnlyViolatedThreeCyclesConstraints=True
    ).create(obj)

    if verbose:
        visitor = obj.multicutVerboseVisitor(1)
        ret = solver.optimize(visitor=visitor)
    else:
        ret = solver.optimize()

    t_inf = time.time() - t_inf

    mc_energy = obj.evalNodeLabels(ret)
    return ret, mc_energy, t_inf


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
        max_iter = 2500):
    write_to_opengm('./tmp.gm')
    t_inf = time.time()

    binary = '/home/constantin/Work/software/bld/LP_MP/solvers/multicut/multicut_opengm_srmp_cycle'
    #subprocess.call([
    output = subprocess.check_output([
        binary,
        '-i', './tmp.gm',
        '--tighten',
        '--tightenReparametrization', 'damped_uniform',
        '--roundingReparametrization', 'damped_uniform',
        '--tightenIteration', '10',
        '--tightenInterval', '100',
        '--tightenSlope', '0.02',
        '--tightenConstraintsPercentage', '0.1',
        '--primalComputationInterval', '100',
        '--maxIter', str(max_iter)
        ],
        shell = True
    )
    t_inf = time.time() - t_inf
    # TODO parse commandline out put to get the primal and lower bound
    os.remove('./tmp.gm')
    return _, _, t_inf


def run_mc_mp_pybindings(n_var, uv_ids, costs,
        max_iter = 2500):

    # dirty hack for lp_mp pybindings
    import sys
    sys.path.append('/home/constantin/Work/software/bld/LP_MP/python')
    import lp_mp

    # nifty graph and objective for node labels and energy
    g = nifty.graph.UndirectedGraph(int(n_var))
    g.insertEdges(uv_ids)
    assert g.numberOfEdges == costs.shape[0], "%i , %i" % (g.numberOfEdges, costs.shape[0])
    assert g.numberOfEdges == uv_ids.shape[0], "%i, %i" % (g.numberOfEdges, uv_ids.shape[0])
    obj = nifty.graph.multicut.multicutObjective(g, costs)

    multicut_opts = lp_mp.solvers.MulticutOptions(maxIter = max_iter)
    t_inf = time.time()
    # FIXME make this compatible with numpy arrays for uv_ids too
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
