import vigra
import numpy as np

def read_graph(path, key):
    n_nodes = vigra.readHDF5(path, '%s/number-of-vertices' % key)
    uv_ids  = vigra.readHDF5(path, '%s/edges' % key)

    if uv_ids.max() + 1 != n_nodes:
        print "Loading graph from:", path
        print "Graph is NOT consecutive"

    return n_nodes, uv_ids

def read_edge_vals(path):
    edge_vals = []
    with open(path) as f:
        for line in f:
            edge_vals.append(float(line))
    return np.array(edge_vals)


def read_model(graph_path, edge_path):
    weights  = read_edge_vals(edge_path)
    n_nodes, uv_ids = read_graph(graph_path, 'graph')
    assert len(uv_ids) == len(weights)
    return n_nodes, uv_ids, weights


def compare_models(graph_a, edges_a, graph_b, edges_b):
    print "Comparing:"
    print graph_a, edges_a
    print "with"
    print graph_b, edges_b

    nodes_a, uvs_a, weigths_a = read_model(graph_a, edges_a)
    nodes_b, uvs_b, weights_b = read_model(graph_b, edges_b)

    assert nodes_a == nodes_b
    assert uvs_a.shape == uvs_b.shape, "%s, %s" % (uvs_a.shape, uvs_b.shape)
    assert (uvs_a == uvs_b).all(), "Agree: %i / %i" % ( np.sum((uvs_a == uvs_b).all(axis = 1)), len(uvs_a))
    assert np.allclose(weigths_a, weights_b)
    print "Passed"


def find_matching_row_indices(x, y):
    assert isinstance(x, np.ndarray)
    assert isinstance(y, np.ndarray)
    # using a dictionary, this is faster than the pure np variant
    indices = []
    rows_x = { tuple(row) : i  for i, row in enumerate(x) }
    for i, row in enumerate(y):
        if tuple(row) in rows_x:
            indices.append( [ rows_x[tuple(row)], i ] )
    return np.array(indices)


# -> for the models the checks
def check_against_original_model(sample, graph_path, edge_path):

    # read test model
    n_nodes, uv_ids, weights = read_model(graph_path, edge_path)

    # read original model
    uv_ids_orig  = vigra.readHDF5('./models/%s_uvs.h5' % sample , 'data')
    weights_orig = vigra.readHDF5('./models/%s_costs.h5' % sample , 'data')
    n_nodes_orig  = uv_ids_orig.max() + 1

    assert n_nodes_orig == n_nodes

    assert uv_ids.shape == uv_ids_orig.shape, "%s, %s" % (uv_ids.shape, uv_ids_orig.shape)

    ## match the uv ids and make sure that they perfectly match
    #uv_ids = np.sort(uv_ids, axis = 1)
    #uv_ids_orig = np.sort(uv_ids_orig)
    #matches = find_matching_row_indices(uv_ids, uv_ids_orig)
    #assert len(matches) == len(uv_ids), "%i, %i" % (len(matches), len(uv_ids))

    #uv_ids = uv_ids[matches[:,0]]
    #weights = weights[matches[:,0]]

    #assert uv_ids.shape == uv_ids_orig.shape, "%s, %s" % (uv_ids.shape, uv_ids_orig.shape)
    #assert (uv_ids == uv_ids_orig).all(), "Agree: %i / %i" % ( np.sum((uv_ids == uv_ids_orig).all(axis = 1)), len(uv_ids))
    assert np.allclose(weights, weights_orig)
    print "Passed"

if __name__ == '__main__':
    check_against_original_model(
            'sampleA',
            './debug/graph_nifty.h5',
            './debug/edgevals_nifty.txt')
    compare_models(
            './debug/graph_py.h5',
            './debug/edgevals_py.txt',
            './debug/graph_nifty.h5',
            './debug/edgevals_nifty.txt')
