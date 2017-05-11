import opengm
from nifty_solver import nifty_mc_objective

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
        primalComputationInterval = 13
        ):
    write_to_opengm(n_var, uv_ids, costs, './tmp.gm')

    # TODO with or without odd_wheel ?
    home_dir = os.path.expanduser("~")
    binary_odd_wheel = os.path.join(home_dir, 'Work/software/bld/LP_MP/src/solvers/multicut/multicut_opengm_srmp_cycle_odd_wheel')
    binary           = os.path.join(home_dir, 'Work/software/bld/LP_MP/src/solvers/multicut/multicut_opengm_srmp_cycle')

    options =  [
        binary_odd_wheel,
        '-i', './tmp.gm',
        '--standardReparametrization', standardReparametrization,
        '--tightenReparametrization',  tightenReparametrization,
        '--roundingReparametrization', roundingReparametrization,
        '--tightenIteration', str(tightenIteration),
        '--tightenInterval', str(tightenInterval),
        '--tightenSlope', str(tightenSlope),
        '--tightenConstraintsPercentage', str(tightenConstraintsPercentage),
        '--primalComputationInterval', str(primalComputationInterval),
        '--maxIter', str(max_iter)
    ]
    if tighten:
        options.append('--tighten')
    if timeout > 0:
        options.extend(['--timeout', str(timeout)])
    if n_threads > 1:
        options.extend(['--numLpThreads', str(n_threads)])

    t_inf = time.time()
    out = subprocess.check_output(
    #subprocess.call(
        options
    )
    t_inf = time.time() - t_inf

    out = out.split('\n')
    l_energy = out[-4].split()
    energy = float(l_energy[-1])

    #print out[-10:]
    #energy = -100

    os.remove('./tmp.gm')
    return np.zeros(n_var), energy, t_inf


def run_mc_mp_pybindings(n_var, uv_ids, costs,
        max_iter = 1000,
        timeout  = 0,
        n_threads= 1,
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


    # dirty hack for lp_mp pybindings
    home_dir = os.path.expanduser("~")
    import sys
    sys.path.append( os.path.join(home_dir, 'Work/software/bld/LP_MP/python') )
    import lp_mp

    # nifty graph and objective for node labels and energy
    obj = nifty_mc_objective(n_var, uv_ids, costs)

    # FIXME make this compatible with numpy arrays for uv_ids too
    t_inf = time.time()
    mc_edges = lp_mp.solvers.multicutMp(
            [(uv[0],uv[1]) for uv in uv_ids],
            costs,
            maxIter = max_iter,
            timeout = timeout,
            standardReparametrization = standardReparametrization,
            tightenReparametrization  = tightenReparametrization,
            roundingReparametrization = roundingReparametrization,
            tightenIteration          = tightenIteration,
            tightenInterval           = tightenInterval,
            tightenSlope              = tightenSlope,
            tightenConstraintsPercentage = tightenConstraintsPercentage,
            primalComputationInterval = primalComputationInterval,
            nThreads                  = n_threads
        )
    t_inf = time.time() - t_inf

    # edge labels to node labels
    merge_edges = uv_ids[np.array(mc_edges) == False]
    ufd = nifty.ufd.ufd(n_var)
    ufd.merge(merge_edges)
    mc_nodes = ufd.elementLabeling()

    mc_energy = obj.evalNodeLabels(mc_nodes)

    return mc_nodes, mc_energy, t_inf
