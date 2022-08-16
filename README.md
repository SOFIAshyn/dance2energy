# dance2energy
## Dance energy style transfer using image-to-image translation networks
Dance2Energy is a project that shows the usage of
AlphaPose ML model and represents the idea of 
Generative Art in two senses: algorithmic & intellectual.

**The concept:**
* Algorithmic Generative Art - generation of the dataset based on the
image data, functional calculations, and usage of Perlin noise.
* Intellectual Generative Art - generation of the images based only on the 
paired data input given to the GAN.

**Result:**

The final result of the project is the image translation of 
original images of dancers into energy flow visuals. On the image below
shown the results of the Algorithmic Generative Art. How one original image is 
translated into abstract image.

<p align="center">
    <img src='/reports/figures/examples_of_pairs.jpeg' width="300">
</p>

In the video below shown the result of Intellectual Generative Art 
generation with Cycle GAN image-to-image translation.

**Press on the image to follow the demo video in YouTube:**
[![Cycle GAN performance](https://img.youtube.com/vi/ZpkNwWG8qWo/0.jpg)](https://www.youtube.com/watch?v=ZpkNwWG8qWo)

- Linux or macOS
- Python 3
- CPU or NVIDIA GPU + CUDA CuDNN

## Table of Contents
  * [Installation](#installation)
  * [Implementation from scratch](#run-the-project-from-skratch)
    + [Data processing](#data-processing)
    + [Implementation from scratch](#implementation-from-scratch)
      + [Step 1: Take a dataset with people dancing](#step-1-take-a-dataset-with-people-dancing)
      + [Step 2: Get the additional data about images with Pose Estimation Model](#step-2-get-the-additional-data-about-images-with-pose-estimation-model)
      + [Step 3: Generate abstractions dataset based on Pose Estimation data](#step-3-generate-abstractions-dataset-based-on-pose-estimation-data)
      + [Step 4: Visualise data with p5.js](#step-4-visualise-data-with-p5js)
    + [Train or use pre-trained GAN models](#train-or-use-pre-trained-gan-models)
      + [BiCycle GAN](#bicycle-gan)
      + [Cycle GAN](#cycle-gan)
    + [Run frame interpolation model](#run-frame-interpolation-model)

# Installation
- Clone the repository:
   ```bash
   git clone https://github.com/SOFIAshyn/dance2energy.git
   cd dance2energy
   ```
- Install [PyTorch](http://pytorch.org) and 0.4+ and other dependencies (e.g., torchvision, [visdom](https://github.com/facebookresearch/visdom) and [dominate](https://github.com/Knio/dominate)).
  - For pip users, please type the command `pip install -r requirements.txt`.
  - For Conda users, you can create a new Conda environment using `conda env create -f environment.yml`.

If you wish to try out the final result, you should follow [**these instructions**](src/models/pytorch-CycleGAN-and-pix2pix/README.md), if you want to generate the datasets and to try to train BiCycle GAN and Cycle GAN, please follow the instructions below.

# Run the project from skratch
## Data processing
**Steps:**
  - Take a dataset with people dancing
  - Get the additional data about images with Pose Estimation Model
  - Generate abstractions dataset based on Pose Estimation data
  - Visualise data with p5.js

## Implementation from scratch

### Step 1: Take a dataset with people dancing
For the pose estimation of your data, you can follow this notebook 
`alphapose_frames_processing.ipynb`.\
You will get data in `.JSON` format about the keypoints of the bodies at the image.\
\
Otherwise, you can work with dancing dataset:
   - Download the dataset [Let's Dance](https://www.cc.gatech.edu/cpl/projects/dance/).
   - Remain `./data/raw/ballet` folder in data. 
   - Follow the instructions from `alphapose_frames_processing.ipynb`.

\
Running these commands you will get: `./data/interim/json_files_each_video` directory.

An example of the images of the dataset:
<p align="center">
    <img src='/reports/figures/lets_dance.jpeg' width="300">
</p>

### Step 2: Get the additional data about images with Pose Estimation Model

* Tracking the same pose is done:
   - Run the command
   ```bash
     cd ./src/data/   
     python3 create_pairs_with_optical_flow.py
   ```
   - You will get `./data/interim/df_pairs_each_video` directory as an output.

* To see flow of vectors from one frame to another, run script:
   ```bash
   cd ./src/data/
   python3 vectors_between_frames_visualisation.py   
   ```
**TODO: add image of vectors transition example.**

* So far we were processing all the `ballet` files. For future GAN usage, 
we will need only the files with one person on the frame. We manually have 
choose the list of directories where only one person is shown. To filter the data, run the script:
   ```bash
   cd ./src/data/
   python3 gan_ballet_image_selector.py
   ```
   You will get data in the directory: `./data/interim/gan_frames`, where each `.JSON` 
file belongs to its directory of the name of the video.

## Step 3: Generate abstractions dataset based on Pose Estimation data

* For future dataset generation with `p5.js` the following data preparation step 
was done: `get_vectors_coordinates_for_p5_js.ipynb`.\
   - Run all the cells, as an output we are getting the following directory: 
`./data/external/p5_df_probs_pairs_5` with `.JSON` file for each video. Each file
describes the flow from one frame to another.
   - Move all the `.JSON` files from this directory into: 
   `./src/visualisation/sketch/assets`.
   
* In `./src/visualisation/sketch` directory is placed the script to generate 
abstraction dataset for processed data with `p5.js`.

## Step 4: Visualise data with p5.js
1. Open `Processsing`. Set up `p5.js` with an editor on the computer. 
2. Open `./src/visualisation/sketch` and run.
   After the run you will get `./data/processed/gan_abstractions` with 
a list of directories of the names of each video.
3. See the comparison of original frame and algorithmically generated 
abstraction image running the cells in 
`./notebooks/abstraction_original_comparison.ipynb`.\
**TODO: add images origVSframe examples.**

## Train or use pre-trained GAN models

### BiCycle GAN
The idea is to teach BiCycle GAN to generate abstractions without all the steps above needed. For the instructions, follow [**this link**](src/models/PyTorch-GAN/README.md).

### Cycle GAN
The idea is to teach Cycle GAN to generate abstractions without all the steps above needed. For the instructions, follow [**this link**](src/models/pytorch-CycleGAN-and-pix2pix/README.md).

## Run frame interpolation model
For the instructions, please follow [**this link**](src/models/frame-interpolation4large-motion/README.md).

### Citation
```bash
@InProceedings{
 CastroDance2017,
 author = {Daniel Castro, Steven Hickson, Patsorn Sangkloy, Bhavishya Mittal, Sean Dai, James Hays and Irfan Essa},
 title = {Let's Dance: Learning From Online Dance Videos},
 booktitle = {eprint arXiv:2139179},
 year = {2018},
}
```







