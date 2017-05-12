import matplotlib.pyplot as plt

import cPickle as pickle
import vigra

def parse_out_niftyfm(out):
    out = out.split('\n')

    energies  = []
    run_times = []
    iter_without_improvement = []

    for line in out[1:]:
        if not line.startswith('Energy:'):
            if line.startswith('end inference'):
                break
            else:
                continue
        values = line.split()
        energies.append(float(values[1]))
        run_times.append(int(values[3]))
        iter_without_improvement.append( int(float(values[5])) )

    return energies, run_times, iter_without_improvement


def parse_out_niftyilp(out):
    out = out.split('\n')

    energies  = []
    run_times = []
    n_violated = []

    for line in out[1:]:
        if not line.startswith('Energy:'):
            if line.startswith('end inference'):
                break
            else:
                continue
        values = line.split()
        energies.append(float(values[1]))
        run_times.append(int(values[3]))
        n_violated.append( int(float(values[5])) )

    return energies, run_times, n_violated


def parse_out_mcmp(out):
    out = out.split('\n')

    primal    = []
    dual      = []
    rt_primal = []
    rt_dual   = []
    dual_improvements = []

    for line in out:
        if line.startswith('best triplet'):
            line = line.split()
            dual_improvements.append(line[-1])

        if not line.startswith('iteration'):
            continue

        line = line.split()
        iter_num    = int(''.join(c for c in line[2] if c.isdigit()))
        lower_bound = float(''.join(c for c in line[6] if c.isdigit() or c == '-'))
        run_time   = float(''.join(c for c in line[-1] if c.isdigit() or c == '.'))

        rt_dual.append(run_time)
        dual.append(lower_bound)

        if line[7] == 'upper':
            val = line[10] if not line[10] == 'inf,' else '0'
            primal.append(
                float(''.join(c for c in val if c.isdigit() or c == '-'))
            )
            rt_primal.append(run_time)

    # postprocess the primals for a better plot and drop primals that have 0 value
    primal = np.array(primal)
    rt_primal = np.array(rt_primal)
    mask = primal != 0
    primal = primal[mask]
    rt_primal = rt_primal[mask]

    return rt_primal, primal, rt_dual, dual, dual_improvements


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


def sampleD_plots(with_dual = False):
    for sample in ('sampleD_medium', 'sampleD_large'):
        times = [
                #vigra.readHDF5(   './anytime_data/%s_fm.h5' % sample,  'run_times'),
                vigra.readHDF5(   './anytime_data/%s_mcmp_py.h5'% sample, 'rt_primal')
        ]
        energies = [
                #vigra.readHDF5('./anytime_data/%s_fm.h5'% sample,   'energies'),
                vigra.readHDF5('./anytime_data/%s_mcmp_py.h5'% sample, 'primal')
        ]
        labels = [
                #'fm',
                'mcmp-primal'
                ]

        if with_dual:
            times.append( vigra.readHDF5(   './anytime_data/%s_mcmp_py.h5'% sample, 'rt_dual') )
            energies.append( vigra.readHDF5('./anytime_data/%s_mcmp_py.h5'% sample, 'dual'))
            labels.append('mcmp-dual')

        plot_energies_sample(
                times,
                energies,
                labels,
                sample)


if __name__ == '__main__':
    #nifty_vs_mcmp(with_dual = True)
    sampleD_plots()
