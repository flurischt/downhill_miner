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
for i, im in enumerate(filter(lambda x: 'jpg' in x, os.listdir('images/'))):
    image = Image.open('images/' + im).convert('L')
    data = np.array(image).copy()
    if data.mean() < 100:  # skip black images
        continue
    if not avg:
        avg = image
    else:
        avg = Image.blend(avg, image, 1.0/float(i+1))

#avg.show()
#avg = np.array(avg.convert('RGBA'))
avg = np.array(avg).copy()

for im in filter(lambda x: 'jpg' in x, os.listdir('images/')):
    image = Image.open('images/' + im)
# TODO: compute a mask (see below) and use only pixels that belong to the rider for clustering
#    # create a b/w image-mask where white=foreground and black=background
#    bw = image.convert('L')
#    mask = np.array(bw).copy()
#    mask = np.absolute(mask - avg)
#    mask[mask < 200] = 0
#    mask[mask >= 200] = 255
#    #new_image = Image.fromarray(mask).show()
#    # only keep masked pixels
#    orig = np.array(image)
#    orig[:,:,0][mask != 255] = 0
#    orig[:,:,1][mask != 255] = 0
#    orig[:,:,2][mask != 255] = 0
#    orig = Image.fromarray(orig)
    orig = image
    width, height = orig.size
    cropped = orig.crop((int(width/4), int(height/5), int(3*width/4), int(2*height/3)))
    cropped.save('cropped/' + im.replace('jpg', 'bmp'))
