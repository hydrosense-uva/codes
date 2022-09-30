from PIL import Image
from pathlib import Path
import glob
import os

#Define path with files
path  = r'C:\Users\robin\Box\HMA\Results\Precipitation\Timeseries\means'
#Access all files with correct 
files = sorted(list(glob.glob(path+'/*.png')))

frames=[]
for i in files:
    new_frame=Image.open(i)
    frames.append(new_frame)

#Name your GIF & Select duration (in ms)
frames[0].save(path+'\\mean_precip_sources_00_16.gif', format='GIF',append_images=frames[1:],save_all=True,duration=800,loop=0)
