import matplotlib.pyplot as plt

import cPickle as pickle
import vigra

def plot_energies_sample(times, energies, labels, title):
    assert len(times) == len(energies)
    assert len(times) == len(labels)
    f, ax = plt.subplots()
    for i, t in enumerate(times):
        en = energies[i]
        ax.plot(t, en, label = labels[i])
    ax.set_xlabel('runtimes [s]')
    ax.set_ylabel('energy')
    ax.set_title('title')
    ax.legend()
    plt.show()


if __name__ == '__main__':
    sample = 'sampleA'
    times = [vigra.readHDF5(   './anytime_data/%s_fm.h5' % sample,   'run_times'),
             vigra.readHDF5(   './anytime_data/%s_mcmp.h5'% sample, 'rt_primal'),
             vigra.readHDF5(   './anytime_data/%s_mcmp.h5'% sample, 'rt_dual')]
    energies = [vigra.readHDF5('./anytime_data/%s_fm.h5'% sample,   'energies'),
                vigra.readHDF5('./anytime_data/%s_mcmp.h5'% sample, 'primal'),
                vigra.readHDF5('./anytime_data/%s_mcmp.h5'% sample, 'dual')]
    plot_energies_sample(
            times,
            energies,
            ['fm', 'mcmp-primal', 'mcmp-dual'],
            sample)
