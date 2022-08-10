'''
14/04/2022

We got Alpha Pose results in 'json_files'. The data was batched, but not batched for each video separately.
So this script filters the data into each video batch.
'''
import json
import os
import pandas as pd


def read_json(json_file, json_path):
    '''
    Read JSON & Return a list of each image each skeleton objects.
    return: list(dict)
    '''
    json_file = open(os.path.join(json_path, json_file), 'r')
    json_load_obj = json.load(json_file)
    json_file.close()
    return json_load_obj


def img_name_to_video_name(img_name):
    return img_name[:-8]


if __name__ == '__main__':
    all_frames_img_ids = []
    dir_of_files_to_sort = '../data/interim/json_files'
    for json_file in sorted(os.listdir(dir_of_files_to_sort)):
        print('Working with JSON file: ', json_file)
        if json_file == '.DS_Store':
            continue
        json_list_of_keypoints_dicts = read_json(json_file, dir_of_files_to_sort)
        df = pd.DataFrame(json_list_of_keypoints_dicts)
        frames_img_ids = sorted(set(df['image_id']))
        all_frames_img_ids += frames_img_ids

    videos_ids = set()
    for img_name in all_frames_img_ids:
        video_name = img_name_to_video_name(img_name)
        videos_ids.add(video_name)

    dir_of_new_json_files = '../data/interim/json_files_each_video'
    for video_name in videos_ids:
        video_images_dictionaries = []
        json_video_dir = os.path.join(dir_of_new_json_files, video_name)
        for json_file in sorted(os.listdir(dir_of_files_to_sort)):
            print('Working with JSON file: ', json_file)
            if json_file == '.DS_Store':
                continue
            json_list_of_keypoints_dicts = read_json(json_file, dir_of_files_to_sort)
            for img_dict in json_list_of_keypoints_dicts:
                if img_name_to_video_name(img_dict['image_id']) == video_name:
                    video_images_dictionaries.append(img_dict)
        # save a new json file
        json_object = json.dumps(video_images_dictionaries, indent=5)
        final_json_file = json_video_dir + '.json'
        with open(final_json_file, "w+") as outfile:
            outfile.write(json_object)