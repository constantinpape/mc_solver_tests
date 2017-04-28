from  utils import write_to_opengm, read_from_mcppl
import vigra
import os

def convert_to_opengm(sample):
    uv_path   = './models/sample%s_uvs.h5' % sample
    cost_path = './models/sample%s_costs.h5' % sample
    assert os.path.exists(uv_path), uv_path
    assert os.path.exists(cost_path), cost_path

    n_var, uvs, costs = read_from_mcppl(uv_path, cost_path)
    write_to_opengm(n_var, uvs, costs, './models/sample%s_opengm.gm')


if __name__ == '__main__':
    for sample in ('A', 'B', 'C'):
        convert_to_opengm(sample)
