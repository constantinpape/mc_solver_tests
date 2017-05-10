# TODO minImprovements
default_multiprocessing = {
        tighten   : True,
        standardReparametrization : 'anisotropic',
        tightenReparametrization  : 'damped_uniform',
        roundingReparametrization : 'damped_uniform',
        tightenIteration          : 2,
        tightenInterval           : 49,
        tightenSlope              : 0.1,
        tightenConstraintsPercentage : 0.05,
        primalComputationInterval : 13
        #,minDualImprovement        : 0
        #,minDualImprovementInterval: 0
}


default_pybindings = {
        primalComputationInterval : 50,
        standardReparametrization : "anisotropic",
        roundingReparametrization : "damped_uniform",
        tightenReparametrization  : "damped_uniform",
        tighten                   : True,
        tightenInterval           : 50,
        tightenIteration          : 5,
        tightenSlope              : 0.1,
        tightenConstraintsPercentage : 0.05
        #,minDualImprovement        : 0
        #,minDualImprovementInterval: 0
}


default_nifty = {
    primalComputationInterval : 100,
    standardReparametrization : "anisotropic",
    roundingReparametrization : "damped_uniform",
    tightenReparametrization  : "damped_uniform",
    tighten : True,
    tightenInterval : 100,
    tightenIteration : 10,
    tightenSlope : 0.02,
    tightenConstraintsPercentage : 0.1
    #,minDualImprovement : 0.
    #,minDualImprovementInterval : 0
}
