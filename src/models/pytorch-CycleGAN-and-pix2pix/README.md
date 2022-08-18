# CycleGAN in PyTorch
<p align="center">
  <img src="https://junyanz.github.io/CycleGAN/images/teaser_high_res.jpg" width="800"/>
</p>

## Table of Contents
+ [Virtual environment setup](#virtual-environment-setup)
+ [Cycle GAN](#cyclegan)
  + [Abstract](#abstract)
  + [Links](#links)
  + [Authors](#authors)
+ [Run example](#run-example)
  + [Prerequisites](#prerequisites)
  + [Installation](#installation)
  + [Cycle GAN tran and test](#cyclegan-train-and-test)
    + [Download the datasets](#download-the-datsets)
    + [Train a model](#train-a-model)
    + [Apply a pre-trained model](#apply-a-pre-trained-model)
    + [Test the model](#test-the-model)
  + [Results](#results)
  + [Experiments](#ex)
+ [Results summary](#results-summary)

## Cycle GAN
### Abstract
This PyTorch implementation produces results comparable to or better than our original Torch software. If you would like to reproduce the same results as in the papers, check out the original [CycleGAN Torch](https://github.com/junyanz/CycleGAN) code.

### Links
[[Project]](https://junyanz.github.io/CycleGAN/) 
[[Paper]](https://arxiv.org/pdf/1703.10593.pdf)
[[Torch]](https://github.com/junyanz/CycleGAN)
[[Tensorflow Core Tutorial]](https://www.tensorflow.org/tutorials/generative/cyclegan)
[[PyTorch Colab]](https://colab.research.google.com/github/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/CycleGAN.ipynb)

### Authors
The code was written by [Jun-Yan Zhu](https://github.com/junyanz) and [Taesung Park](https://github.com/taesungp), and supported by [Tongzhou Wang](https://github.com/SsnL).

Harry Yang, Archit Rathore, Van Huy, Xiaowei Hu, Zhenliang He, luoxier, zsdonghao, Yanghua Jin, yunjey, tjwei, Simon Karlsson, Ldpe2G.

## Run example
**Note**: The current software works well with PyTorch 1.4. Check out the older [branch](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/tree/pytorch0.3.1) that supports PyTorch 0.1-0.3.

### Prerequisites
- Linux or macOS
- Python 3
- CPU or NVIDIA GPU + CUDA CuDNN

### Installation
- After cloning the whole repository install the requirements
- Install [PyTorch](http://pytorch.org) and 0.4+ and other dependencies (e.g., torchvision, [visdom](https://github.com/facebookresearch/visdom) and [dominate](https://github.com/Knio/dominate)).
  - For pip users, please type the command `pip install -r requirements.txt`.
  - For Conda users, you can create a new Conda environment using `conda env create -f environment.yml`.

### CycleGAN train and test
#### Download the datasets
- Download a CycleGAN dataset (e.g. `dance2energy128` & `dance2energy256`):
  - Download dataset of images in size 128 pixels
  ```bash
  cd ./datasets
  wget https://drive.google.com/file/d/1jdwy89ewIeKONgTT5faVF2pODnl1jY7W/view?usp=sharing ./
  unzip dance2energy128.zip -d ./
  ```
  - Download dataset of images in size 256 pixels
  ```bash
  cd ./datasets
  wget https://drive.google.com/file/d/1wZHJ7rJEAk8TnDuRpvE7ZfhrznAhFwBv/view?usp=sharing ./
  unzip dance2energy256.zip -d ./
  ```
- To view training results and loss plots, run `python -m visdom.server` and click the URL http://localhost:8097.
- To log training progress and test images to W&B dashboard, set the `--use_wandb` flag with train and test script

#### Train a model
  - Test the model (dataset 128 px):
    ```bash
    #!./scripts/test_cyclegan.sh
    python test.py --dataroot ./datasets/dance2energy128 --name dance2energy_cyclegan128 --model cycle_gan --phase test --no_dropout
    ```
    - The test results will be saved to a html file here: `./results/dance2energy_cyclegan128/latest_test/index.html`.

  - Test the model (dataset 256 px):
    ```bash
    #!./scripts/test_cyclegan.sh
    python test.py --dataroot ./datasets/dance2energy256 --name dance2energy_cyclegan256 --model cycle_gan --phase test --no_dropout
    ```
    - The test results will be saved to a html file here: `./results/dance2energy_cyclegan256/latest_test/index.html`.
    
#### Apply a pre-trained model
You can download a pretrained model (e.g. dance2energy) with the following script:
- Model for images input in size of 128px: 
    ```bash
    cd ./checkpoints
    wget https://drive.google.com/file/d/15HP3NAyG2Ievs708EPEnfARfnqU4hnQ_/view?usp=sharing dance2energy_cyclegan128
    unzip dance2energy_cyclegan128.zip -d ./
    ```
- The pretrained model is saved at `./checkpoints/dance2energy_cyclegan128/latest_net_G.pth`.
- Model for images input in size of 256px: 
    ```bash
    cd ./checkpoints
    wget https://drive.google.com/file/d/1vN17HVutyM2tgXqaD1sXprn1CVuyHUWh/view?usp=sharing dance2energy_cyclegan
    unzip dance2energy_cyclegan.zip -d ./
    ```
- The pretrained model is saved at `./checkpoints/dance2energy_cyclegan/latest_net_G.pth`.

#### Test the model
- To test the model, you also need to download the dance2energy dataset:
  - Download (dataset 128 px)
    ```bash
    cd ./datasets
    wget https://drive.google.com/file/d/1jdwy89ewIeKONgTT5faVF2pODnl1jY7W/view?usp=sharing ./
    unzip dance2energy128.zip -d ./
    ```
  - Download (dataset 256 px)
    ```bash
    cd ./datasets
    wget https://drive.google.com/file/d/1wZHJ7rJEAk8TnDuRpvE7ZfhrznAhFwBv/view?usp=sharing ./
    unzip dance2energy256.zip -d ./
    ```

- Then generate the results using
  - Test the model (dataset 128 px):
      ```bash
      #!./scripts/test_cyclegan.sh
      python test.py --dataroot ./datasets/dance2energy128/testA --name dance2energy_cyclegan128 --model cycle_gan --phase test --no_dropout
      ```
    The test results will be saved to a html file here: `./results/dance2energy_cyclegan128/latest_test/index.html`.

  - Test the model (dataset 256 px):
    ```bash
    #!./scripts/test_cyclegan.sh
    python test.py --dataroot ./datasets/dance2energy256/testA --name dance2energy_cyclegan256 --model cycle_gan --phase test --no_dropout
    ```
    The test results will be saved to a html file here: `./results/dance2energy_cyclegan256/latest_test/index.html`.

- The option `--model test` is used for generating results of CycleGAN only for one side. This option will automatically set `--dataset_mode single`, which only loads the images from one set. On the contrary, using `--model cycle_gan` requires loading and generating results in both directions, which is sometimes unnecessary. The results will be saved at `./results/`. Use `--results_dir {directory_path_to_save_result}` to specify the results directory.
pix_dataset.sh facades

- Note that we specified `--direction BtoA` as Facades dataset's A to B direction is photos to labels.

- If you would like to apply a pre-trained model to a collection of input images (rather than image pairs), please use `--model test` option. See `./scripts/test_single.sh` for how to apply a model to Facade label maps (stored in the directory `facades/testB`).

### Results
After the run, you will see the results in
`./results/dance2energy_cyclegan/test_latest/images`
directory.

### Experiments
All the experiments were run on the images dataset, that was cut into squeres.
The main idea was to cut images into squeres in order to use general access Cycle GAN model.
It was done in order to check how can be machine tought how to generate `itself perviously generated` abstractions.
Size of the images that were given to training is 128px. On all the images the person was in the middle of the frame.
<p align="center">
    <img src="../../../reports/figures/cycle.png" width="600"\>
</p>
Here you can see the video of the abstractions generated with Cycle GAN, and marged together with FILM interpolation technique (click on the image):

[![Cycle GAN performance](https://img.youtube.com/vi/ZpkNwWG8qWo/0.jpg)](https://www.youtube.com/watch?v=ZpkNwWG8qWo)



## Results summary
According to the analysis of the work done, we investigated the Image-to-Image translation problem on images of real life and abstract generated images. We have noticed that if we take a pair of complex images as an input, we need more epochs for a model to learn the patterns of the desired outputs. If the size of images is 256, the pattern of energy flow is learned much better for complex ’dance2energy’ and easier ’danceSkeleton2energy’. The other side of Image-to-Image translation models is the mode collapse problem; BiCycle GAN aims to avoid this problem with the offered architecture. However, what we have noticed is that the network is prone to have a mode collapse, only working in smaller latent space; with the smaller size of image inputs, the model performs better results.

## Citation
```
@inproceedings{CycleGAN2017,
  title={Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks},
  author={Zhu, Jun-Yan and Park, Taesung and Isola, Phillip and Efros, Alexei A},
  booktitle={Computer Vision (ICCV), 2017 IEEE International Conference on},
  year={2017}
}


@inproceedings{isola2017image,
  title={Image-to-Image Translation with Conditional Adversarial Networks},
  author={Isola, Phillip and Zhu, Jun-Yan and Zhou, Tinghui and Efros, Alexei A},
  booktitle={Computer Vision and Pattern Recognition (CVPR), 2017 IEEE Conference on},
  year={2017}
}
```
