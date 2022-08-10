'''
25/04/2022 - Sofiia Petryshyn
We have a flow from one frame to another one. This flow is implemented with skeleton tracking.
To keep an eye on the results the visualisation is necessary.

The module is to have vectors visualised from the previous frame to the current one.
'''
import json
import os
import pandas as pd
import numpy as np
from toolz.functoolz import compose
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def create_vectors_for_visualisation(df, verbose=False):
    def get_34_vector_pairs(prev_keypoints_from, cur_keypoints_to):
        '''
        We have this structure for each keypont: [x, y, score].
        We are ignoring 'score' field that we get to this vector.
        We are returning the list of 34 elements:
        return: list((prev_x1, cur_x1), (prev_y1, cur_y1), ... (prev_x17, cur_x17), (prev_y17, cur_y17))
        '''
        vectors_to_draw_x_y_coordinates = list(zip(prev_keypoints_from, cur_keypoints_to))
        lst = list(range(51))
        indexes_to_drop = lst[2::3]
        if verbose:
            print('before:', len(vectors_to_draw_x_y_coordinates))
        new_vectors_to_draw_x_y_coordinates = []
        for i, x_y_coord in enumerate(vectors_to_draw_x_y_coordinates):
            if i in indexes_to_drop:
                continue
            new_vectors_to_draw_x_y_coordinates.append(x_y_coord)
        assert len(new_vectors_to_draw_x_y_coordinates) == 34
        if verbose:
            print('after:', len(new_vectors_to_draw_x_y_coordinates))
            print(new_vectors_to_draw_x_y_coordinates)
        return new_vectors_to_draw_x_y_coordinates

    def get_17_vectors(prev_keypoints_from, cur_keypoints_to):
        '''
        After the first function call, we are getting... :
        We are getting this structure:
        list((prev_x1, cur_x1), (prev_y1, cur_y1), ... (prev_x17, cur_x17), (prev_y17, cur_y17))
        
        return: [(prev_x1, prev_y1), ... , (prev_x17, prev_y17)],
                [(cur_x1, cur_y1), ... ,   (cur_x17, cur_y17)  ]
        ''' 
        lst_to_reconstruct = get_34_vector_pairs(prev_keypoints_from, cur_keypoints_to)
        prev_x_y = [el[0] for el in lst_to_reconstruct]
        cur_x_y = [el[1] for el in lst_to_reconstruct]
        all_prev_x, all_prev_y = prev_x_y[::2], prev_x_y[1::2]
        all_cur_x, all_cur_y = cur_x_y[::2], cur_x_y[1::2]
        final_list_prev, final_list_cur = list(zip(all_prev_x, all_prev_y)), list(zip(all_cur_x, all_cur_y))
        return final_list_prev, final_list_cur
        
    def calculate_directions(final_list_prev_x_y, final_list_cur_x_y):
        '''
        Return directions of each keypoint.
        return: [(x1, y1), (x2, y2), ... (x17, y17)]
        '''
        vector_of_17_dir = []
        for i in range(len(final_list_prev_x_y)):
            prev_x, prev_y = final_list_prev_x_y[i][0], final_list_prev_x_y[i][1]
            cur_x, cur_y = final_list_cur_x_y[i][0], final_list_cur_x_y[i][1]
            dir_coord = calc_dir(cur_x, cur_y, prev_x, prev_y)
            vector_of_17_dir.append(dir_coord)
        return vector_of_17_dir
    
    def calc_dir(cur_x, cur_y, prev_x, prev_y):
        return np.array((cur_x, cur_y)) - np.array((prev_x, prev_y))
    
    def draw_vectors(starting_points, direction_list, \
                     path_to_orig_images, prev_skeleton_name, cur_skeleton_name, \
                     verbose=False):
        def show_orig_from_and_to_images(path_to_orig_images, prev_skeleton_name, cur_skeleton_name):
            img = mpimg.imread(os.path.join(path_to_orig_images, prev_skeleton_name))
            imgplot = plt.imshow(img)
            plt.title(prev_skeleton_name)
            plt.show()
            img = mpimg.imread(os.path.join(path_to_orig_images, cur_skeleton_name))
            imgplot = plt.imshow(img)
            plt.title(cur_skeleton_name)
            plt.show()
        
        def get_canvas_size(path_to_orig_images, prev_skeleton_name):
            img = mpimg.imread(os.path.join(path_to_orig_images, prev_skeleton_name))
            return img.shape
        
        V = np.array(direction_list)
        if verbose:
            print('starting_points = ', starting_points)
            print('direction_list = ', direction_list)
        origin = np.array([[coord_tup[0] for coord_tup in starting_points],\
                           [coord_tup[1] for coord_tup in starting_points]])
        canvas_size = get_canvas_size(path_to_orig_images, prev_skeleton_name)
        plt.axis([0, canvas_size[1], canvas_size[0], 0])
        plt.quiver(*origin, V[:,0], V[:,1], color=['r','b','g'], angles='xy', scale_units='xy', scale=1)
        plt.show()
        show_orig_from_and_to_images(path_to_orig_images, prev_skeleton_name, cur_skeleton_name)
        

    path_to_orig_images = '../data/ballet/'
    # for each row, where we have pairs
    for i in tqdm(df.index):
        row = df.loc[i, :]
        print(f'Going from a frame {row.prev_skeleton_name} to a frame {row.cur__skeleton_name}:')
        prev_keypoints_from = [float(number)for number in row.prev_keypoints_from[1:-1].split(', ')]
        cur_keypoints_to = [float(number)for number in row.cur_keypoints_to[1:-1].split(', ')]
        final_list_prev_x_y, final_list_cur_x_y = get_17_vectors(prev_keypoints_from, cur_keypoints_to)
        starting_points = final_list_prev_x_y
        direction_list = calculate_directions(final_list_prev_x_y, final_list_cur_x_y)
        draw_vectors(starting_points, direction_list,\
                     path_to_orig_images, row.prev_skeleton_name, \
                     row.cur__skeleton_name)



if __name__ == '__main__':
    path_to_final_pairs = '../data/df_pairs_each_video'
    os.makedirs(path_to_final_pairs, exist_ok=True)

    for pair_csv_file in sorted(os.listdir(path_to_final_pairs)):
        print(f'Working with this file: {os.path.join(path_to_final_pairs, pair_csv_file)}')
        if pair_csv_file == '.ipynb_checkpoints':
            continue
        df = pd.read_csv(os.path.join(path_to_final_pairs, pair_csv_file))
        create_vectors_for_visualisation(df)
        

