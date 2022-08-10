# 20/04/22 - Sofiia Petryshyn
# Here we build a skeleton tracker.
# We connect every skeleton from previous video frame to the current one.
# Here we just connect the closest skeleton to the other closest skeleton on the next image.
#
# we have a bunch of json files,
# and we read each of them to get more data
import json
import os
import pandas as pd
import numpy as np


def read_json(json_file):
    '''
    Read JSON & Return a list of each image each skeleton objects.
    return: list(dict)
    '''
    json_file = open(os.path.join(jsonS_path, json_file), 'r')
    return json.load(json_file)


def compare_keypoints_and_create_pairs(prev_keypoints, cur_keypoints):
    '''
    Get summed distance between (prev_keypoints & cur_keypoints)
    len(prev_keypoints): 51
    len(cur_keypoints): 51
    Dimention of prev_keypoint (same for cur_keypoints):
        len = number of skeletons detected on the same image
        len of each keypoint array = 17 * 3
        , where for each keypoint we have [x, y, score]
    return: summmed distance of each keypoint in prev & cur keypoints
    '''
    dist_array = []
    for i in range(int(len(prev_keypoints) / 3)):  # max i = 16, so last (x,y,c) = 48,49,50
        # notation: point = np.array((x, y))
        point1 = np.array((prev_keypoints[i * 3], prev_keypoints[i * 3 + 1]))
        point2 = np.array((cur_keypoints[i * 3], cur_keypoints[i * 3 + 1]))

        dist = np.linalg.norm(point1 - point2)
        dist_array.append(dist)
    return np.sum(dist_array)


class Pair:
    def __init__(self, prev_keypoint_id, \
                 cur_keypoint_id, sum_of_dist_btw_keypoints, \
                 from_img, to_img, \
                 keypairs_from, keypairs_to):
        self.prev_keypoint_id = prev_keypoint_id
        self.cur_keypoint_id = cur_keypoint_id
        self.sum_of_dist_btw_keypoints = sum_of_dist_btw_keypoints
        self.from_img = from_img
        self.to_img = to_img
        self.keypairs_from = keypairs_from
        self.keypairs_to = keypairs_to

    def to_dict(self):
        return {
            'prev_keypoint_id': self.prev_keypoint_id,
            'cur_keypoint_id': self.cur_keypoint_id,
            'sum_of_dist_btw_keypoints': self.sum_of_dist_btw_keypoints,
            'from_img': self.from_img,
            'to_img': self.to_img,
            'keypairs_from': self.keypairs_from,
            'keypairs_to': self.keypairs_to
        }

    def __repr__(self, flag_full=True):
        if flag_full is False:
            return f'''
            prev_keypoint_id: {self.prev_keypoint_id};
            cur_keypoint_id: {self.cur_keypoint_id};
            sum_of_dist_btw_keypoints: {self.sum_of_dist_btw_keypoints};
            from_img: {self.from_img};
            to_img: {self.to_img};
            '''
        else:
            return f'''
            prev_keypoint_id: {self.prev_keypoint_id};
            cur_keypoint_id: {self.cur_keypoint_id};
            sum_of_dist_btw_keypoints: {self.sum_of_dist_btw_keypoints};
            from_img: {self.from_img};
            to_img: {self.to_img};
            keypairs_from: {self.keypairs_from};
            keypairs_to: {self.keypairs_to}
            '''


def sort_pairs_by_smallest_dist(list_of_pairs):
    '''
    Sorted from a smaller distance between points to a larger distance
    '''
    return sorted(list_of_pairs, key=lambda pair: pair.sum_of_dist_btw_keypoints)


def create_pairs(sorted_pairs_by_dist):
    final_pairs = []
    used_i, used_j = set(), set()
    for pair in sorted_pairs_by_dist:
        if (pair.prev_keypoint_id not in used_i) and \
                (pair.cur_keypoint_id not in used_j):
            final_pairs.append(pair)
            used_i.add(pair.prev_keypoint_id)
            used_j.add(pair.cur_keypoint_id)
    return final_pairs


if __name__ == '__main__':
    res_df_dir = '../data/interim/df_pairs_each_video'
    jsonS_path = '../data/interim/json_files_each_video'
    jsonS_list = sorted(os.listdir(jsonS_path))

    for i_json, json_file in enumerate(jsonS_list):
        res_df_path = os.path.join(res_df_dir, json_file[:-5] + '.csv')
        frames = []
        if json_file == '.DS_Store':
            continue
        print('Working with JSON file: ', json_file)

        json_list_of_keypoints_dicts = read_json(json_file)
        df = pd.DataFrame(json_list_of_keypoints_dicts)
        frames_img_ids = sorted(set(df['image_id']))
        pev_image_name, image_name = frames_img_ids[0], frames_img_ids[0]
        # ***
        # 0005: if there are 7 people detected
        # all_samples_prev_keypoints would have 7 items to iterate
        # ***
        all_samples_prev_keypoints = df[df['image_id'] == image_name]['keypoints'].tolist()
        list_of_pairs = []
        json_united_list_of_final_pairs = []
        next_json_keypoints_exist_flag = 0
        # we iterate over each 0005 -> 0010 -> 0015 ...
        for i, image_name in enumerate(frames_img_ids[1:]):
            print('\tFROM image sample: ', pev_image_name)
            print('\tTO   image sample: ', image_name)
            all_samples_cur_keypoints = df[df['image_id'] == image_name]['keypoints'].tolist()

            for i, prev_keypoints in enumerate(all_samples_prev_keypoints):
                for j, cur_keypoints in enumerate(all_samples_cur_keypoints):
                    # compare keypoints & create pairs
                    sum_of_dist_btw_keypoints = compare_keypoints_and_create_pairs(prev_keypoints, cur_keypoints)
                    pair = Pair(i, j, sum_of_dist_btw_keypoints, \
                                from_img=pev_image_name, to_img=image_name, \
                                keypairs_from=prev_keypoints, keypairs_to=cur_keypoints
                                )
                    list_of_pairs.append(pair)
            # algorithm to choose there there are the smallest distances btw keypoints
            sorted_pairs_by_dist = sort_pairs_by_smallest_dist(list_of_pairs)
            list_of_final_pairs = create_pairs(sorted_pairs_by_dist)
            # TODO: rank by bounding boxes overlap.
            # This step can be done to improve the algorithm , not needed so far
            # ***
            print(f'''
            ***************************
            Found final pairs list for {pev_image_name} &
                                       {image_name}
            ***************************
            ''')
            # ***
            # TODO: save a table of pairs with keypoints
            # to table 'list_of_final_pairs'
            # ***
            df_final_pairs = pd.DataFrame.from_records([pair.to_dict() for pair in list_of_final_pairs])
            frames.append(df_final_pairs)

            pev_image_name = image_name
            prev_keypoints = cur_keypoints
        # save pairs file
        df_final_pairs_merged = pd.concat(frames)
        df_final_pairs_merged.to_csv(res_df_path, index=False)
    #         break
    #         print(list_of_final_pairs[0])
    #         break
    #     df['area'] = df.apply(lambda x: x['box'][-1]*x['box'][-2], axis=1)
    #     df['x'] = df.apply(lambda x: x['box'][0], axis=1)
    #     df['y'] = df.apply(lambda x: x['box'][1], axis=1)
    #     df['w'] = df.apply(lambda x: x['box'][2], axis=1)
    #     df['l'] = df.apply(lambda x: x['box'][3], axis=1)
    #     df.drop(['category_id', 'score', 'idx', 'box'], axis=1, inplace=True)

    #     for image_name in set(df['image_id']):
    #         print(df[df['image_id'] == image_name]['image_id'])
    #         break
    #     break
