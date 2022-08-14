from PIL import Image
import os

if __name__ == '__main__':
    video_dir = '6813'
    new_video_dir = 'testB'
    full_path1 = '/home/sofiiapetryshyn/dance-gan/PyTorch-GAN/data/inference'
    full_path2 = '/home/sofiiapetryshyn/dance-gan/pytorch-CycleGAN-and-pix2pix/datasets/dance2energy256'

    full_video_dir = os.path.join(full_path1, video_dir)
    full_new_video_dir = os.path.join(full_path2, new_video_dir)
    for frame in os.listdir(full_video_dir):
        print('Working with .. ', frame)
        img = Image.open(os.path.join(full_video_dir, frame))
        w, h = img.size[0], img.size[1]
        left, right = (int((w - h)/2), int((w - h)/2)) if not (w - h) % 2 else (int((w - h)/2), int((w - h)/2+1))
        box = (left, 0, h+right, h)
        img2 = img.crop(box)
        img2 = img2.resize((256, 256))
        img2.save(os.path.join(full_new_video_dir, frame))
        print("Saved: ", os.path.join(full_new_video_dir, frame))
