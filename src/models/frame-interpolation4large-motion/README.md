# FILM: Frame Interpolation for Large Motion

After we run Cycle GAN model, the model [FILM](https://github.com/google-research/frame-interpolation) was used.
To interpolate in between of the generated samples and to represent a video as a reference.

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

As a result we got this video (click on the image):
[![Cycle GAN performance](https://img.youtube.com/vi/ZpkNwWG8qWo/0.jpg)](https://www.youtube.com/watch?v=ZpkNwWG8qWo)


## Citation
If you find this implementation useful in your works, please acknowledge it appropriately by citing:
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