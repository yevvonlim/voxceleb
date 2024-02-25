# download frames from youtube videos
# @Author: Yewon Lim
# @Date: 2024-02-25
# run 'pip install vidgear' to install vidgear
# 'pip install yt_dlp' to install yt_dlp

import cv2
import os
from vidgear.gears import CamGear
import argparse
import os.path as osp
from typing import Union, List
import pandas as pd 
from io import StringIO



# parse arguments
def parse_args():
    parser = argparse.ArgumentParser(description='Download frames from youtube videos')
    parser.add_argument('--data_root', type=str, required=True, help='Path to the root directory of the dataset')
    args = parser.parse_args()
    return args

# download frames from youtube videos
def download_frames(uid, save_path, ann_df:pd.DataFrame):
    '''Params]
    uid: str, unique identifier of the video (youtube video id)
    save_path: str, path to save the frames
    start_frame: int, starting frame number
    end_frame: int, ending frame number
    bbox: list, bounding box of the face in the format [x, y, w, h]
    '''
    # open stream
    stream = CamGear(source=f"https://www.youtube.com/watch?v={uid}",
                     stream_mode=True, 
                     logging=True,
    ).start()

    current_frame = 0
    idx=-1
    # loop over
    while True:
        current_frame += 1
        # read frames from stream
        frame = stream.read()
        # check if frame is None
        if frame is None:
            break
        if current_frame < ann_df['FRAME'].iloc[0]:
            continue
        if current_frame > ann_df['FRAME'].iloc[-1]:
            break
        idx += 1
        if idx >= len(ann_df):
            break
        fname = ann_df['FNAME'].iloc[idx]
        w, h, x, y = ann_df['W'].iloc[idx], ann_df['H'].iloc[idx], ann_df['X'].iloc[idx], ann_df['Y'].iloc[idx]
        if not osp.exists(osp.join(save_path, fname)):
            os.makedirs(osp.join(save_path, fname, 'cropped'), exist_ok=True)
            os.makedirs(osp.join(save_path, fname, 'uncropped'), exist_ok=True)
        # save frame
        cv2.imwrite(osp.join(save_path, fname, f'uncropped/{current_frame:06d}.jpg'), frame)

        # crop the face and resize it to 224x224
        # annotation asuumes the video resolution is 360p 
        H, W = frame.shape[:2]
        scale = 360 / H
        x, y, w, h = int(x * scale), int(y * scale), int(w * scale), int(h * scale)
        # print(frame.shape, scale, x, y, w, h)
        # frame = cv2.resize(frame, (360, int(W*scale)))
        face = frame[y:y+h, x:x+w, :]
        face = cv2.resize(face, (224, 224))
        cv2.imwrite(osp.join(save_path, fname, f'cropped/{current_frame:06d}.jpg'), face)

    # close stream
    stream.stop()


def txts2df(txt_paths:List[str]):
    '''Convert txt files to a single dataframe'''
    txts = [open(txt_path, 'r').readlines() for txt_path in txt_paths]
    txts = ['\n'.join(txt[6:]) for txt in txts]
    dfs = [pd.read_csv(StringIO(txt), sep='\t') for txt in txts]
    for i, df in enumerate(dfs):
        # remove space in the column names
        for k in df.keys():
            df[k.replace(' ', '')] = df[k]
            del df[k]
        df['FNAME'] = osp.basename(txt_paths[i].replace('.txt', ''))
    df = pd.concat(dfs, ignore_index=True).sort_values(by='FRAME', axis=0).reset_index(drop=True)
    print(df.head())
    return df


if __name__ == "__main__":
    # args = parse_args()
    # data_root = args.data_root
    # save_path = osp.join(data_root, 'frames')
    # os.makedirs(save_path, exist_ok=True)
    from glob import glob 
    txt_paths = glob('/home/ubuntu/Projects/yewon/datasets/VoxCeleb/voxceleb1/train/wav/id11240/7k9-JvvuVNY/*.txt')
    ann_df = txts2df(txt_paths)
    # # download frames
    # download_frames(uid='dQw4w9WgXcQ', save_path=save_path, start_frame=0, end_frame=10)
    # print("Frames are downloaded successfully!
    download_frames('7k9-JvvuVNY', '/home/ubuntu/Projects/yewon/datasets/VoxCeleb/voxceleb1/train/wav/id11240/7k9-JvvuVNY', ann_df)