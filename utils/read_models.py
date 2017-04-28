import nifty
import numpy as np
import vigra

def read_from_opengm(model_path):
    pass

def read_from_mcluigi(model_path):
    pass

def read_from_mcppl(uv_path, costs_path):
    uv_ids = vigra.readHDF5(uv_path, 'data')
    # assert uvs are consecutive and start at 0
    uniques = np.unique(uv_ids)
    assert len(uniques) == uniques.max() + 1
    costs  = vigra.readHDF5(costs_path, 'data')
    assert len(costs) == len(uv_ids)
    return uv_ids.max() + 1, uv_ids, costs
