import vigra

rag_path = {
    "sampleA" : '/home/constantin/Work/home_hdd/cache/cremi_pmap_exps/sample_A_train/sample_A_train_cutout_1/rag_seg0.h5',
    "sampleB" : '/home/constantin/Work/home_hdd/cache/cremi_pmap_exps/sample_B_train/sample_B_train_cutout_1/rag_seg0.h5',
    "sampleC" : '/home/constantin/Work/home_hdd/cache/cremi_pmap_exps/sample_C_train/sample_C_train_cutout_1/rag_seg0.h5'
    }

def project_to_seg(sample, node_res, save_path):
    rag = vigra.graphs.loadGridRagHDF5(rag_path[sample], 'rag')
    seg = rag.projectLabelsToBaseGraph(node_res.astype('uint32'))
    vigra.writeHDF5(seg, save_path, 'data', compression = 'gzip')


