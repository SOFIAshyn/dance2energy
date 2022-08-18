# FILM: Frame Interpolation for Large Motion
Tensorflow 2 implementation of our high quality frame interpolation neural network. We present a unified single-network approach that doesn't use additional pre-trained networks, like optical flow or depth, and yet achieve state-of-the-art results. We use a multi-scale feature extractor that shares the same convolution weights across the scales. Our model is trainable from frame triplets alone.

## Table of Contents
* [Abstract](#abstract)
* [Links](#links)
* [Authors](#authors)
* [Run example](#run-example)
  * [Results](#results)
* [Citation](#citation)

## Abstract
After we run Cycle GAN model, the model [FILM](https://github.com/google-research/frame-interpolation) was used.
FILM was used in order to interpolate in between of the generated samples and to represent a video as a reference.

## Links
[[Project]](https://github.com/google-research/frame-interpolation#project--paper--youtube--benchmark-scores-) 
[[Paper]](https://arxiv.org/pdf/2202.04901.pdf) 
[[YouTube]](https://www.youtube.com/watch?v=OAD-BieIjH4)
[[Benchmark Scores]](https://github.com/google-research/frame-interpolation)

## Authors
Fitsum Reda, Janne Kontkanen, Eric Tabellion, Deqing Sun, Caroline Pantofaru, Brian Curless, Google Research, University of Washington.

## Run example

To convert images to the same size this code was used:
`1hdHc1hJAWU_005_` - the name of the image frames directory to process.
```bash
mkdir 1hdHc1hJAWU_005_500 && convert "1hdHc1hJAWU_005_/*.jpg[500x]" -set filename:base "%[basename]" "1hdHc1hJAWU_005_500/%[filename:base].jpg"
```

To check that the size was changed, run this command:
```bash
identify 1hdHc1hJAWU_005_500/1hdHc1hJAWU_005_0010.jpg
```

To do interpolation in between of the frames, clone [FILM](https://github.com/google-research/frame-interpolation) repository and run this command:
```bash
python3 -m frame_interpolation.eval.interpolator_cli --pattern "<path to the directory of the grames for the interpolation>" --model_path pretrained_models/film_net/Style/saved_model --times_to_interpolate 6 --output_video
```

### Results
As a result we got this video (click on the image):

[![Cycle GAN performance](https://img.youtube.com/vi/ZpkNwWG8qWo/0.jpg)](https://www.youtube.com/watch?v=ZpkNwWG8qWo)


## Citation
```
@article{reda2022film,
 title = {FILM: Frame Interpolation for Large Motion},
 author = {Fitsum Reda and Janne Kontkanen and Eric Tabellion and Deqing Sun and Caroline Pantofaru and Brian Curless},
 booktitle = {The European Conference on Computer Vision (ECCV)},
 year = {2022}
}
```
```
@misc{film-tf,
  title = {Tensorflow 2 Implementation of "FILM: Frame Interpolation for Large Motion"},
  author = {Fitsum Reda and Janne Kontkanen and Eric Tabellion and Deqing Sun and Caroline Pantofaru and Brian Curless},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/google-research/frame-interpolation}}
}
```