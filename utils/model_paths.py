model_paths_new = {
    'sampleA' : ('../models/sampleA_uvs.h5', '../models/sampleA_costs.h5'),
    'sampleB' : ('../models/sampleB_uvs.h5', '../models/sampleB_costs.h5'),
    'sampleC' : ('../models/sampleC_uvs.h5', '../models/sampleC_costs.h5'),
}

model_paths_new_opengm = {
    'sampleA' : '../models/sampleA_opengm.gm',
    'sampleB' : '../models/sampleB_opengm.gm',
    'sampleC' : '../models/sampleC_opengm.gm',
}

model_paths_mcluigi = {
    'sampleD_sub_L1'   : '/home/constantin/Work/home_hdd/cache/cache_luigi/sampleD_subsample2/ReducedProblem_50_512_512_modifed.h5',
    'sampleD_sub_full' : '/home/constantin/Work/home_hdd/cache/cache_luigi/sampleD_subsample2/MulticutProblem_modifed.h5',
    'sampleD_L4'       : '/home/constantin/Work/home_hdd/cache/cache_luigi/sampleD/ReducedProblem_400_4096_4096_modifed.h5',
    'sampleD_L3'       : '/home/constantin/Work/home_hdd/cache/cache_luigi/sampleD/ReducedProblem_200_2048_2048_modifed.h5',
    'sampleD_L2'       : '/home/constantin/Work/home_hdd/cache/cache_luigi/sampleD/ReducedProblem_100_1024_1024_modifed.h5',
    'sampleD_L1'       : '/home/constantin/Work/home_hdd/cache/cache_luigi/sampleD/ReducedProblem_50_512_512_modifed.h5',
    'sampleD_full'     : '/home/constantin/Work/home_hdd/cache/cache_luigi/sampleD/MulticutProblem_modifed.h5'
}

mode_paths_lifted = {
    'isbi' : {'local_uvs'   : '../models/lifted_models/isbi/uv_ids_local.h5',
              'lifted_uvs'  : '../models/lifted_models/isbi/uv_ids_lifted.h5',
              'local_costs' : '../models/lifted_models/isbi/costs_local.h5',
              'lifted_costs': '../models/lifted_models/isbi/costs_lifted.h5'
              },
    'snemi' :{'local_uvs'   : '../models/lifted_models/snemi/uv_ids_local.h5',
              'lifted_uvs'  : '../models/lifted_models/snemi/uv_ids_lifted.h5',
              'local_costs' : '../models/lifted_models/snemi/costs_local.h5',
              'lifted_costs': '../models/lifted_models/snemi/costs_lifted.h5'
              }
}
