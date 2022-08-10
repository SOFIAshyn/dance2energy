import subprocess
import shlex

dir_ballet = '../data/raw/ballet/'
dir_ballet_for_gan = '../data/interim/gan_frames/'
os.makedirs(dir_ballet_for_gan, exist_ok=True)
list_of_one_person_dancing_videos = ['1hdHc1hJAWU_005_', '2OcaeW67VIc_030_', '3xjpYjLO1aM_030_', '9ZNFPk60yjE_232_', 'B-DUOlHKKVU_005_', 'BVM8AP3luyI_015_', 'cIFB-GmLGyQ_210_', 'Fo250jmBl6I_005_', 'HwvyKmpTEkg_120_', 'm4A6PLeGIB4_005_', 'nM-rm68GyRk_020_', 'o1eV2Mgc_BI_018_', 'pBAY_XH3sgw_010_', 'S5HwZJQ8NuA_011_', 'SmRrfm1ihGg_008_', 'Wz_f9B4pPtg_020_', 'XAsMB3eRe6g_007_', 'Xj1_aETg6Ww_640_', 'XwmwsGT8IQ4_510_', 'zWBVa2m_4Fs_050_'];
path_to_final_pairs = '../data/interim/df_pairs_each_video/'

if __name__ == '__main__':
    for pair_csv_file in sorted(os.listdir(path_to_final_pairs)):
        if pair_csv_file[:-4] not in list_of_one_person_dancing_videos:
            continue
        frame_dir_for_gan = dir_ballet_for_gan + pair_csv_file[:-4] + '/'
        os.makedirs(frame_dir_for_gan, exist_ok=True)

        print(f'Working with this file: {os.path.join(path_to_final_pairs, pair_csv_file)}')
        if pair_csv_file == '.ipynb_checkpoints':
            continue
        df = pd.read_csv(os.path.join(path_to_final_pairs, pair_csv_file))
        file_names_for_gan = df.cur__skeleton_name.to_list()
        # copy images from file_nmaes_for_gan into frame_dir_for_gan
        for file_name in file_names_for_gan:
            from_file_name = dir_ballet + file_name
            to_file_name = frame_dir_for_gan + file_name
            comm = 'cp ' + from_file_name + ' ' + to_file_name
            print('run command: ', comm)
            subprocess.run(shlex.split(comm))
