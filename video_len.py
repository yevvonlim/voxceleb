import subprocess 
from glob import glob 
from tqdm.auto import tqdm 
from concurrent.futures import ProcessPoolExecutor

files = glob("/data/VoxCeleb2/mp4/*/*/*.mp4")


    

# for file in tqdm(files, total=len(files)):
#     cmd = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {file}"
#     output = subprocess.check_output(cmd, shell=True).decode('utf-8')
#     sec += float(output)

# split files into 16 chunks
# step = len(files) // 16
# chunks = [files[i:i+step] if i+step < len(files) else files[i:] for i in range(0, len(files), step) ]

pool = ProcessPoolExecutor(max_workers=16)
results = list(pool.map(lambda x: sum([float(subprocess.check_output(f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {file}", shell=True).decode('utf-8')) for file in x]), files))
print(f"Total duration: {sum(results) / 3600 :.2f} hours")