# !/bin/bash

for i in 1 2 3 4 5 6
do
    aws s3 cp s3://global-datasets/VoxCeleb/vox2_mp4_$i.zip ./vox2_mp4_$i.zip 
done