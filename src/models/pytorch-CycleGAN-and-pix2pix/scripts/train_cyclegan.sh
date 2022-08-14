set -ex
python train.py --dataroot ./datasets/dance2energy128 --name dance2energy_cyclegan128 --model cycle_gan --pool_size 50 --no_dropout --load_size 128 --crop_size 128
