import matplotlib.pyplot as plt

import cPickle as pickle
import vigra

def plot_energies_sample(times, energies, labels, title):
    assert len(times) == len(energies)
    assert len(times) == len(labels), "%i, %i" % (len(times), len(labels))
    f, ax = plt.subplots()
    for i, t in enumerate(times):
        en = energies[i]
        ax.plot(t, en, label = labels[i])
    ax.set_xlabel('runtimes [s]')
    ax.set_ylabel('energy')
    ax.set_title('title')
    ax.legend()
    plt.show()


# Evaluation showed that pybindings and commandline yield the same results
def mcmp_py_vs_cmd():
    for sample in ('sampleA','sampleB','sampleC'):
        times = [
                 vigra.readHDF5(   './anytime_data/%s_mcmp_py.h5'% sample, 'rt_primal'),
                 vigra.readHDF5(   './anytime_data/%s_mcmp_py.h5'% sample, 'rt_dual'),
                 vigra.readHDF5(   './anytime_data/%s_mcmp_cmd.h5'% sample, 'rt_primal'),
                 vigra.readHDF5(   './anytime_data/%s_mcmp_cmd.h5'% sample, 'rt_dual')
                ]
        energies = [
                    vigra.readHDF5('./anytime_data/%s_mcmp_py.h5'% sample, 'primal'),
                    vigra.readHDF5('./anytime_data/%s_mcmp_py.h5'% sample, 'dual'),
                    vigra.readHDF5('./anytime_data/%s_mcmp_cmd.h5'% sample, 'primal'),
                    vigra.readHDF5('./anytime_data/%s_mcmp_cmd.h5'% sample, 'dual')
                  ]
        plot_energies_sample(
                times,
                energies,
                ['mcmp_py-primal', 'mcmp_py-dual', 'mcmp_py-primal', 'mcmp_py-dual'],
                sample)


def nifty_vs_mcmp(with_dual = False, with_ilp = False):
    for sample in ('sampleA','sampleB','sampleC'):
        times = [
                vigra.readHDF5(   './anytime_data/%s_fm.h5' % sample,  'run_times'),
                vigra.readHDF5(   './anytime_data/%s_mcmp_py.h5'% sample, 'rt_primal')
        ]
        energies = [
                vigra.readHDF5('./anytime_data/%s_fm.h5'% sample,   'energies'),
                vigra.readHDF5('./anytime_data/%s_mcmp_py.h5'% sample, 'primal')
        ]
        labels = ['fm', 'mcmp-primal']

        if with_dual:
            times.append( vigra.readHDF5(   './anytime_data/%s_mcmp_py.h5'% sample, 'rt_dual') )
            energies.append( vigra.readHDF5('./anytime_data/%s_mcmp_py.h5'% sample, 'dual'))
            labels.append('mcmp-dual')


        if with_ilp:
            times.append(vigra.readHDF5('./anytime_data/%s_ilp.h5'% sample, 'run_times'))
            energies.append(vigra.readHDF5('./anytime_data/%s_ilp.h5'% sample, 'energies'))
            labels.append('ilp')

        plot_energies_sample(
                times,
                energies,
                labels,
                sample)


if __name__ == '__main__':
    nifty_vs_mcmp(with_dual = True)
