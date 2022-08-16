# dance2energy
Dance2Energy is a project that shows the usage of
AlphaPose ML model and represents the idea of 
Generative Art in two senses: algorithmical & intelectual.

The final result of the project is translation of original dancing images into energy flow visuals:


<img src="https://junyanz.github.io/CycleGAN/reports/figures/examples_of_pairs.jpeg" width="600"/>
[![Cycle GAN performance](https://youtu.be/ZpkNwWG8qWo)
- Linux or macOS
- Python 3
- CPU or NVIDIA GPU + CUDA CuDNN

## Getting Started
### Installiation
- Clone the repository:
   ```bash
   git clone https://github.com/SOFIAshyn/dance2energy.git
   cd dance2energy
   ```
- Install [PyTorch](http://pytorch.org) and 0.4+ and other dependencies (e.g., torchvision, [visdom](https://github.com/facebookresearch/visdom) and [dominate](https://github.com/Knio/dominate)).
  - For pip users, please type the command `pip install -r requirements.txt`.
  - For Conda users, you can create a new Conda environment using `conda env create -f environment.yml`.

If you wish to [Docker](docs/docker.md)

### Run the project from skratch
#### Prepare data for visualisation
1. For the pose estimation of your data, you can follow this notebook 
`alphapose_frames_processing.ipynb`.\
You will get data in `.JSON` format about the keypoints of the bodies at the image.\
\
Otherwise, you can work with dancing dataset:
   - Download the dataset [Let's Dance](https://www.cc.gatech.edu/cpl/projects/dance/).
   - Remain `./data/raw/ballet` folder in data. 
   - Follow the instructions from `alphapose_frames_processing.ipynb`.

\
Running these commands you will get: `./data/interim/json_files_each_video` directory.

2. Tracking the same pose is done:
   - Run the command
   ```bash
     cd ./src/data/   
     python3 create_pairs_with_optical_flow.py
   ```
   - You will get `./data/interim/df_pairs_each_video` directory as an output.

3. To see flow of vectors from one frame to another, run script:
   ```bash
   cd ./src/data/
   python3 vectors_between_frames_visualisation.py   
   ```
**TODO: add image of vectors transition example.**

4. So far we were processing all the `ballet `files. For future GAN usage, 
we will need only the files with one person on the frame. We manually have 
chose the list of directories where only one person is shown. To filter the data, run the script:
   ```bash
   cd ./src/data/
   python3 gan_ballet_image_selector.py
   ```
   You will get data in the directory: `./data/interim/gan_frames`, where each `.JSON` 
file belongs to its directory of the name of the video.

5. For future dataset generation with `p5.js` the following data preparation step 
was done: `get_vectors_coordinates_for_p5_js.ipynb`.\
   - Run all the cells, as an output we are getting the following directory: 
`./data/external/p5_df_probs_pairs_5` with `.JSON` file for each video. Each file
describes the flow from one frame to another.
   - Move all the `.JSON` files from this directory into: 
   `./src/visualisation/sketch/assets`.
   
6. In `./src/visualisation/sketch` directory is placed the script to generate 
abstraction dataset for processed data with `p5.js`.

### Visualise data with p5.js
1. Open `Processsing`. Set up `p5.js` with an editor on the computer. 
2. Open `./src/visualisation/sketch` and run.
   After the run you will get `./data/processed/gan_abstractions` with 
a list of directories of the names of each video.
3. See the comparison of original frame and algorithmically generated 
abstraction image running the cells in 
`./notebooks/abstraction_original_comparison.ipynb`.\
**TODO: add images origVSframe examples.**

### Prepare data for GANs training











