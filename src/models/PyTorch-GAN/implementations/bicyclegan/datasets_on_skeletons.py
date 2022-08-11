import glob
import os
from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms as transforms
from torchvision.transforms import functional as F
import json


class ImageDataset(Dataset):
    def __init__(self, root, orig, abstract, bbox, input_size, mode='train'):
        self.transform = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
            ]
        )
        self.orig = orig
        self.only_generated_video_directories = [el.split('/')[-1] for el in
                                                 sorted(glob.glob(os.path.join(os.path.join(root, mode), abstract) +
                                                                  "/*"))]
        self.abstract_files = self._get_list_of_images(root, mode, abstract)
        self.orig_files = self._get_list_of_images(root, mode, orig)
        self.bbox_dict = self._get_json_of_sorted_bbox_img_details(root, mode, bbox)
        f = open(os.path.join(os.path.join(root, mode), 'image_sizes.json'), 'r')
        self.width_height_dict = json.load(f)
        f.close()
        self.model_input_size = input_size

    def _get_list_of_images(self, root, mode, img_type):
        list_of_all_names = []

        if img_type == self.orig:
            set_of_images = set([el.split('/')[-1] for el in self.abstract_files])
            for v in set_of_images:
                list_of_all_names.append(
                    os.path.join(os.path.join(os.path.join(os.path.join(root, mode), img_type), v[:-8]),
                                 v[:-3] + 'png'))
            list_of_all_names = sorted(list_of_all_names)
        else:
            for v in self.only_generated_video_directories:
                list_of_all_names += sorted(glob.glob(os.path.join(os.path.join(os.path.join(root, mode),
                                                                                img_type), v) + "/*.*"))
            list_of_all_names = sorted(list_of_all_names)
        return list_of_all_names

    def _get_json_of_sorted_bbox_img_details(self, root, mode, bbox):
        abstract_files_short_path = set([el.split('/')[-1] for el in self.abstract_files])
        bbox_dict = {}
        for v in self.only_generated_video_directories:
            json_path = os.path.join(os.path.join(os.path.join(root, mode), bbox), v.split('/')[-1]) + '.json'
            json_f = open(json_path, 'r')
            json_f_data = json.load(json_f)
            for img_data in json_f_data:
                if img_data['image_id'] in abstract_files_short_path:
                    bbox_dict[img_data['image_id']] = img_data['box']
            json_f.close()
        return bbox_dict

    @staticmethod
    def _get_x_y_for_square(rad, bbox_x):
        if rad - bbox_x >= 0:
            return int(0)
        if rad - bbox_x < 0:
            return int(bbox_x - rad)

    def get_bbox_dict(self):
        return self.bbox_dict

    def __getitem__(self, index):
        indx_of_frame = index % len(self.abstract_files)
        img_abst = Image.open(self.abstract_files[indx_of_frame])
        img_skeleton = Image.open(self.orig_files[indx_of_frame]).convert('RGB')
        frame_name = self.orig_files[indx_of_frame].split('/')[-1][:-3] + 'jpg'
        img_bbox = self.bbox_dict.get(frame_name, None)
        w, h = self.width_height_dict[frame_name[:-8]]
        img_skeleton = self.transform(img_skeleton)
        img_abst = self.transform(img_abst)
        img_skeleton = F.resize(img_skeleton, [h, w])
        img_abst = F.resize(img_abst, [h, w])
        rad = int(h / 2)
        bbox_center_coord = ((img_bbox[0] + img_bbox[0] + img_bbox[2]) / 2,
                             (img_bbox[1] + img_bbox[1] + img_bbox[3]) / 2)
        bbox_x, bbox_y = bbox_center_coord[0], bbox_center_coord[1]
        x_pos = self._get_x_y_for_square(rad, bbox_x)
        # prepare for the model - !!!
        img_skeleton_cropped = F.resized_crop(img_skeleton, top=0, left=x_pos,
                                              height=h, width=h,
                                              size=[self.model_input_size, self.model_input_size],
                                              interpolation=transforms.InterpolationMode.BICUBIC
                                              )
        img_abst_cropped = F.resized_crop(img_abst, top=0, left=x_pos,
                                          height=h, width=h,
                                          size=[self.model_input_size, self.model_input_size],
                                          interpolation=transforms.InterpolationMode.BICUBIC
                                          )
        return {'img_skeleton': img_skeleton_cropped, 'img_abst': img_abst_cropped}

    def __len__(self):
        return len(self.abstract_files)
