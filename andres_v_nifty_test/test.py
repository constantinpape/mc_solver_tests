import nifty
import subprocess
import os
import numpy as np

import sys
sys.path.append('..')
from utils import nifty_mc_objective, model_paths_new, read_from_mcppl

def andres_input(uv_ids, costs):

    with open('./build_andres/tmp_uvs.txt', 'w') as f:
        for uv in uv_ids:
            f.write( "%i %i\n" % (uv[0], uv[1]) )

    with open('./build_andres/tmp_costs.txt', 'w') as f:
        for c in costs:
            f.write( "%f\n" % c )


def read_andres_output():

    edge_labels = []
    with open('./build_andres/tmp_edge_labels.txt') as f:
        out = f.read().split()
        for val in out:
            edge_labels.append(int(val))

    return np.array(edge_labels)


def clear_andres_out():
    os.remove('./build_andres/tmp_edge_labels.txt')

def clear_andres_in():
    os.remove('./build_andres/tmp_uvs.txt')
    os.remove('./build_andres/tmp_costs.txt')


def to_edgelabels(obj, node_res):
    graph = obj.graph
    uv_ids = graph.uvIds()
    edge_labels = node_res[uv_ids[:,0]] != node_res[uv_ids[:,1]]
    assert len(edge_labels) == graph.numberOfEdges
    return edge_labels


def nifty_kl(obj, greedy_ws = False):
    #if greedy_ws:
    #    greedy = obj.greedyAdditiveFactory().create(obj)
    #    res = greedy.optimize()
    #solver = obj.multicutKernighanLinFactory().create(obj)
    #if greedy_ws:
    #    res = solver.optimize(res)
    #else:
    #    res = solver.optimize()
    #return to_edgelabels(obj, res), obj.evalNodeLabels(res)
    solver = obj.multicutAndresKernighanLinFactory(greedyWarmstart = greedy_ws).create(obj)
    res = solver.optimize()
    return to_edgelabels(obj, res), obj.evalNodeLabels(res)


def nifty_gaec(obj):
    #solver = obj.greedyAdditiveFactory().create(obj)
    solver = obj.multicutAndresGreedyAdditiveFactory().create(obj)
    res = solver.optimize()
    return to_edgelabels(obj, res), obj.evalNodeLabels(res)


def energy_from_edge_labels(obj, edge_labels):
    graph = obj.graph
    ufd = nifty.ufd.ufd(graph.numberOfNodes)
    merge_nodes = graph.uvIds()[edge_labels == 0]
    ufd.merge(merge_nodes)
    node_labels = ufd.elementLabeling()
    return obj.evalNodeLabels(node_labels)


def andres_kl(obj, greedy_ws = False):

    subprocess.call(
            ['./build_andres/kernighan-lin',
             './build_andres/tmp_costs.txt',
             './build_andres/tmp_uvs.txt',
             './build_andres/tmp_edge_labels.txt',
             '1' if greedy_ws else '0'
            ])
    edge_labels = read_andres_output()
    clear_andres_out()
    return edge_labels, energy_from_edge_labels(obj, edge_labels)


def andres_gaec(obj):

    subprocess.call(
            ['./build_andres/gaec',
             './build_andres/tmp_costs.txt',
             './build_andres/tmp_uvs.txt',
             './build_andres/tmp_edge_labels.txt'
            ])
    edge_labels = read_andres_output()
    clear_andres_out()
    return edge_labels, energy_from_edge_labels(obj, edge_labels)


def compare_labels(labels_a, labels_b):
    assert len(labels_a) == len(labels_b)
    matches = labels_a == labels_b
    print np.sum(matches), '/'
    print len(labels_a)


def test_nifty_v_andres(sample):

    print sample

    paths = model_paths_new[sample]
    n_var, uv_ids, costs = read_from_mcppl(paths[0], paths[1])

    obj = nifty_mc_objective(n_var, uv_ids, costs)
    andres_input(uv_ids, costs)

    labels_gaec_andres, e_gaec_andres = andres_gaec(obj)
    labels_gaec_nifty, e_gaec_nifty   = nifty_gaec(obj)
    print "Results GAEC:"
    print "Energies:"
    print "Andres:", e_gaec_andres
    print "Nifty: ", e_gaec_nifty
    compare_labels(labels_gaec_nifty, labels_gaec_andres)

    #labels_kl_andres, e_kl_andres = andres_kl(obj)
    #labels_kl_nifty, e_kl_nifty   = nifty_kl(obj)
    #print "Results KL:"
    #print "Energies:"
    #print "Andres:", e_kl_andres
    #print "Nifty: ", e_kl_nifty
    #compare_labels(labels_kl_nifty, labels_kl_andres)

    labels_gaeckl_andres, e_gaeckl_andres = andres_kl(obj, True)
    labels_gaeckl_nifty, e_gaeckl_nifty   = nifty_kl(obj, True)
    print "Results GAEC + KL:"
    print "Energies:"
    print "Andres:", e_gaeckl_andres
    print "Nifty: ", e_gaeckl_nifty
    compare_labels(labels_gaeckl_nifty, labels_gaeckl_andres)

    clear_andres_in()


if __name__ == '__main__':
    for sample in ('sampleA', 'sampleB', 'sampleC'):
        test_nifty_v_andres(sample)
