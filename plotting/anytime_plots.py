import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as mtick
import numpy as np

import cPickle as pickle
import vigra
import sys
sys.path.append('..')
from utils import *

parser = {
        'ilp' : parse_out_niftyilp,
        'fm-ilp' : parse_out_niftyfm,
        'fm-kl' : parse_out_niftyfm,
        'fm-greedy' : parse_out_niftyfm,
        'mp' : parse_out_mcmp,
        'mp-fmkl' : parse_out_mcmp,
        'mp-fmgreedy' : parse_out_mcmp,
        }


def plot_energies_sample(times, energies, labels, title, bounds = None):
    assert len(times) == len(energies)
    assert len(times) == len(labels), "%i, %i" % (len(times), len(labels))
    f, ax = plt.subplots()
    for i, t in enumerate(times):
        en = energies[i]
        ax.plot(t, en, label = labels[i])
    ax.set_xlabel('runtimes [s]')
    ax.set_ylabel('energy')
    ax.set_title(title)
    if bounds is not None:
        ax.set_ylim(bounds)

    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%i'))
    ax.legend()
    ax.get_yaxis().set_major_formatter(
                matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    plt.title(title)
    plt.show()



def sampleD_plots(with_dual = False):

    sample = 'sampleD_sub_full'
    #solvers = ['ilp', 'fm-ilp', 'fm-kl', 'mp', 'mp-fmgreedy']
    solvers = ['fm-ilp', 'fm-kl', 'mp', 'mp-fmgreedy']

    #if with_dual:
    #    times.append( vigra.readHDF5(   './anytime_data/%s_mcmp_py.h5'% sample, 'rt_dual') )
    #    energies.append( vigra.readHDF5('./anytime_data/%s_mcmp_py.h5'% sample, 'dual'))
    #    labels.append('mcmp-dual')

    times = []
    energies = []
    labels = []
    bounds = []
    for solver in solvers:
        out_path = '../tests/anytime_data/sampleD_sub/%s_%s.txt' % (sample, solver)
        t, e = parser[solver](out_path)
        #if solver == 'ilp':
        #    t = t[11:]
        #    e = e[11:]
        assert len(t) == len(e)
        times.append(t)
        energies.append(e)
        labels.append(solver)
        if solver in 'ilp':
            bounds.append( ( np.min(e), np.min(e) ) )
        if solver in ('fm-ilp', 'fm-kl'):
            bounds.append( ( np.min(e),np.max(e) ) )

    bounds = np.array(bounds)
    bounds = [bounds[:,0].min(), round(bounds[:,1].max(),-2)]
    bounds = None

    #title = '%s - ILP: -722692 after 2 iterations (6600 s)' % sample
    title = '%s' % sample
    plot_energies_sample(
            times,
            energies,
            labels,
            title,
            bounds,
            )


if __name__ == '__main__':
    #nifty_vs_mcmp(with_dual = True)
    sampleD_plots()
