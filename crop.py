"""
currently this script just crops the images to an area where the riders are. 
TODO: create bg-image using moving-averages (see below), then find the riders and only use their pixels for clustering 
"""

import os
import shutil
import numpy as np
from PIL import Image

if os.path.exists('cropped/'):
    shutil.rmtree('cropped/')
    os.mkdir('cropped/')

# build a background image using moving-averages
avg = None
i = 0
for im in filter(lambda x: 'jpg' in x, os.listdir('images/')):
    image = Image.open('images/' + im)
    data = np.array(image).copy()
    if data.mean() < 100:  # skip dark (night) images
        continue
    if not avg:
        avg = image
    else:
        avg = Image.blend(avg, image, 1.0/float(i+1))
        i = i+1

#avg.show()
avg = np.array(avg).copy()

for im in list(filter(lambda x: 'jpg' in x, os.listdir('images/'))):
    image = Image.open('images/' + im)
    # compute a 480x640 b/w-mask with pixel=255 => could be an object, pixel=0 => pixel is background
    mask = np.array(image).copy()
    mask = np.absolute(mask - avg)
    bw = Image.fromarray(mask).convert('L')
    mask = np.array(bw)
    mask[mask < 200] = 0
    mask[mask >= 200] = 255
    # now hide everything in the background (make it transparent)
    image.putalpha(Image.fromarray(mask))
    #image.show() # transparency effect not visible here. export to png and have a look at it there
    # crop and export
    width, height = image.size
    cropped = image.crop((int(width/4), int(height/5), int(3*width/4), int(2*height/3)))
    cropped.save('cropped/' + im.replace('jpg', 'png'))
