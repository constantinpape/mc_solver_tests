import vigra

from volumina_viewer import volumina_n_layer
from multicut_src import load_dataset


raw_path = {
    "sampleA" : '/home/constantin/Work/home_hdd/cache/cremi_pmap_exps/sample_A_train/inp0.h5',
    "sampleB" : '/home/constantin/Work/home_hdd/cache/cremi_pmap_exps/sample_B_train/inp0.h5',
    "sampleC" : '/home/constantin/Work/home_hdd/cache/cremi_pmap_exps/sample_C_train/inp0.h5'
    }

ds_path = {
    "sampleA" : '/home/constantin/Work/home_hdd/cache/cremi_pmap_exps/sample_A_train',
    "sampleB" : '/home/constantin/Work/home_hdd/cache/cremi_pmap_exps/sample_B_train',
    "sampleC" : '/home/constantin/Work/home_hdd/cache/cremi_pmap_exps/sample_C_train'
}

def view(sample, res_paths, res_labels):
    assert len(res_paths) == len(res_labels)
    raw = vigra.readHDF5(raw_path[sample], 'data').astype('float32')
    ds  = load_dataset(ds_path[sample])
    bb  = ds.get_cutout(1).bb
    raw = raw[bb]

    data = [raw]
    labels = ['raw']
    for resp in res_paths:
        res = vigra.readHDF5(resp, 'data')
        assert res.shape == raw.shape, "%s, %s" % (str(res.shape), str(raw.shape) )
        data.append(res)
    labels.extend(res_labels)

    volumina_n_layer(data, labels)


if __name__ == '__main__':
    view(
        'sampleA',
        [
        './segmentations/nifty_fm_sampleA.h5',
        './segmentations/nifty_kl_sampleA.h5'
        ],
        ['nifty-fm', 'nifty-kl']
    )
