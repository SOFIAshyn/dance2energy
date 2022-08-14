import os
import shlex
import subprocess
import shutil


def create_test_train_AB(dataset_dir, a2b, testA, testB, trainA, trainB):
    os.chdir(dataset_dir)
    # if os.path.exists(a2b):
    #     shutil.rmtree(a2b)
    if not os.path.exists(a2b):
        os.makedirs(a2b)
    print(f'Made {a2b}')

    os.chdir(os.path.join(dataset_dir, a2b))
    for dir_name in [testA, testB, trainA, trainB]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            os.makedirs(dir_name)
    print(f'Made AB folders')


def create_folders_AB(origA, origB, dataset_dir, a2b):
    '''
    Run the commands to replace images to the directories trainA, trainB, testA, testB
    To train Cycle GAN.
    :param origA: str - a person dancing (./data/ballet)
    :param origB: str - an abstraction (./data/png_files)
    :param dataset_dir: str
    :return: None
    '''
    set_A = set(os.listdir(origA))
    print(list(set_A)[:10])
    print(origB)
    abstract_sorted_files = sorted(os.listdir(origB))
    len_abstract_sorted_files = len(abstract_sorted_files)
    print(len_abstract_sorted_files)
    stop_train_idx = len_abstract_sorted_files * 80 / 100

    dataset_dir = os.path.join(dataset_dir, a2b)
    dir_to_move_A = os.path.join(dataset_dir, trainA)
    dir_to_move_B = os.path.join(dataset_dir, trainB)
    for i, fileB in enumerate(abstract_sorted_files):
        if i > stop_train_idx and dir_to_move_A != os.path.join(dataset_dir, testA):
            dir_to_move_A = os.path.join(dataset_dir, testA)
            dir_to_move_B = os.path.join(dataset_dir, testB)
            print("SWITCH WAS HERE"*100)
        # print(fileB)
        fileA = fileB[4:-3] + 'jpg'
        if fileA not in set_A:
        # try:
        #     assert fileA in set_A, f"'{fileA}' doesn't exist in {origA} directory. Chek if '{fileB}' is a proper one."
        # except AssertionError:
            print(f"{fileA} doesn't exist in {origA} directory. Chek if '{fileB}' is a proper one.")
            continue
        fileA = os.path.join(origA, fileA)
        fileB = os.path.join(origB, fileB)
        # move fileA from dirA to datasets/trainA
        # move fileB from dirB to datasets/trainB

        comm = "cp " + fileA + " " + dir_to_move_A
        print(comm)
        subprocess.run(shlex.split(comm))
        comm = "cp " + fileB + " " + dir_to_move_B
        print(comm)
        subprocess.run(shlex.split(comm))


if __name__ == '__main__':
    init_dir = os.getcwd()
    print("HERE: ", init_dir)
    orig_data_dir, dataset_dir, a2b = '../data/', 'datasets/', 'people2abstract'
    orig_data_dir, dataset_dir = os.path.join(init_dir, orig_data_dir),\
                                 os.path.join(init_dir, dataset_dir)
    # os.chdir(os.path.join(here, orig_data_dir))
    dirA, dirB = 'ballet', 'png_files_every_thr'
    origA, origB = os.path.join(orig_data_dir, dirA), os.path.join(orig_data_dir, dirB)
    testA, testB, trainA, trainB = 'testA', 'testB', 'trainA', 'trainB'

    create_test_train_AB(dataset_dir, a2b, testA, testB, trainA, trainB)
    create_folders_AB(origA, origB, dataset_dir, a2b)
    # os.listdir(origB)




