import numpy as np
import vigra

def read_labelfile(labelfile, stop, converter = int):
    edge_labels = []
    with open(labelfile) as f:
        inp = f.read().split()
    this_labels = []
    for i, ll in enumerate(inp):
       if ll != stop:
           this_labels.append(converter(ll))
       else:
           edge_labels.append(np.array(this_labels))
           this_labels = []
    return edge_labels


def check_labels(edge_labels):
    for i, ee in enumerate(edge_labels):
        print "Labels", i, '/', len(edge_labels)
        print ee.shape


def compare_labels(labels_a, labels_b):
    assert labels_a.shape == labels_b.shape
    print np.sum( np.isclose(labels_a, labels_b) ), '/'
    print len(labels_a)


if __name__ == '__main__':
    print "lpmp"
    lpmp_labels = read_labelfile('./tests/labeling_lpmp.txt', '2')
    lpmp_labels_in = read_labelfile('./tests/labeling_lpmp_in.txt', 'A', float)
    check_labels(lpmp_labels)

    print "nifty"
    nifty_labels = read_labelfile('./tests/labeling_nifty.txt', '2')
    nifty_labels_in = read_labelfile('./tests/labeling_nifty_in.txt', 'A', float)
    check_labels(nifty_labels)

    compare_labels(lpmp_labels_in[0], nifty_labels_in[0])
    compare_labels(lpmp_labels[0], nifty_labels[0])
    #compare_labels(lpmp_labels[-1], nifty_labels[-1])
