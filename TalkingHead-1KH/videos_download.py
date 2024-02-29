import argparse
import multiprocessing as mp
import os
from functools import partial
from time import time as timer

from pytube import YouTube
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--input_list', type=str, required=True,
                    help='List of youtube video ids')
parser.add_argument('--output_dir', type=str, default='data/youtube_videos',
                    help='Location to download videos')
parser.add_argument('--num_workers', type=int, default=16,
                    help='How many multiprocessing workers?')
args = parser.parse_args()


def download_video(output_dir, video_id):
    r"""Download video."""
    video_path = '%s/%s.mp4' % (output_dir, video_id)
    if not os.path.isfile(video_path):
        try:
            # Download the highest quality mp4 stream.
            yt = YouTube('https://www.youtube.com/watch?v=%s' % (video_id),)
                        #  request_headers={'cookie': 'ns=yt&el=adunit&cpn=1oJ25nigKl8rWjFE&ver=2&cmt=5.368&fmt=399&fs=0&rt=78.802&adformat=15_2_1&content_v=sDDHIu6nwUs&euri&lact=39&cl=610595970&state=paused&volume=67&cbrand=apple&cbr=Chrome&cbrver=122.0.0.0&c=WEB&cver=2.20240224.11.00&cplayer=UNIPLAYER&cos=Macintosh&cosver=10_15_7&cplatform=DESKTOP&autoplay=1&final=1&delay=28&hl=ko_KR&cr=KR&uga=m24&len=90.021&afmt=251&idpj=-1&ldpj=-1&st=5.368&et=5.368&muted=0&docid=aS2C1K3W4WQ&ei=2YbfZYKqA5yM0-kPl-2DqAY&plid=AAYSdf9dsG8E8cZo&referrer=https%3A%2F%2Fwww.youtube.com%2F&sdetail=p%3A%2F&sourceid=y&aqi=2IbfZbukKfeX7OsPuI4y&of=Mg8W3EO7C5lVkSK-XkCiUA&vm=CAEQABgEOjJBSHFpSlRKTFRjZU80UzBFRDBXOFhzckxxZmN0WXlZazJkSUxvOFA2OHdMYmxqcF9XUWJuQVBta0tESXpKN1JMUk5qZWxsREdjOWJ1SkJDdTlRdm1fTWx4bGVrZndhTHBXRHVYMFBuc0Vwc1FKMkhIWTlzZ3d5ejZ1elFKb1FZMWpRSXU0eVVrM3RLRVplZzFkUWtuTTBvejVUU1BFYURBd2doAg&host_cpn=BSYaRrpVBQsvEEmb'})
            stream_vid = yt.streams.filter(subtype='mp4', only_video=True, adaptive=True).first()
            stream_audio = yt.streams.filter(subtype='mp4', only_audio=True, adaptive=True).first()

            stream_vid.download(output_path=output_dir, filename=video_id + '.mp4')
            stream_audio.download(output_path=output_dir, filename=video_id + '.aac')
        except Exception as e:
            print(e)
            print('Failed to download %s' % (video_id))
    else:
        print('File exists: %s' % (video_id))


if __name__ == '__main__':
    # Read list of videos.
    video_ids = []
    with open(args.input_list) as fin:
        for line in fin:
            video_ids.append(line.strip())

    # Create output folder.
    os.makedirs(args.output_dir, exist_ok=True)

    # Download videos.
    downloader = partial(download_video, args.output_dir)

    start = timer()
    pool_size = args.num_workers
    print('Using pool size of %d' % (pool_size))
    with mp.Pool(processes=pool_size) as p:
        _ = list(tqdm(p.imap_unordered(downloader, video_ids), total=len(video_ids)))
    print('Elapsed time: %.2f' % (timer() - start))
