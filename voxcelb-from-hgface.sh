# !/bin/bash

# for i in 1 2 3 4 5 6
# do
#     # wget -O /home/ubuntu/datasets/VoxCeleb/vox2_mp4_$i.zip https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_mp4_$i.zip 
#     aria2c -s16 -x16 -d $1 -o vox2_mp4_$i.zip https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_mp4_$i.zip 
# done

for i in 1 2
do 
    aria2c -s16 -x16 -d $1 -o vox2_aac$i.zip https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_aac_$i.zip
done


aria2c -s16 -x16 -d $1 -o vox2_test_mp4.zip https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_test_mp4.zip
aria2c -s16 -x16 -d $1 -o vox2_test_aac.zip https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox2/vox2_test_aac.zip
