"""
try to cluster the cropped/* image into K clusters (configure the number of clusters below).
after clustering the original images are copied into clustered/CLUSTER_INDEX/
"""

import os
import shutil
import numpy as np
from PIL import Image

from sklearn import cluster

# the number of clusters
K=15


def normalize_columns(columns):
    """
    normalize the size of all columns by repeating the last pixel-value
    TODO: this probably repeats only pixels of the B channel...
    """
    max_rows = max(map(lambda x: x.size, columns))
    normalized_columns = []
    for col in columns:
        rows = col.size 
        if rows < max_rows:
            col = np.concatenate((col, np.repeat(col[rows-1], max_rows-rows)))
        assert col.size == max_rows
        normalized_columns.append(col)
    return normalized_columns


def build_matrix():
    """
    creates a matrix where each column is a list of pixels per image. 
    we only use non-transparent pixels. so, every pixel with alpha=0 is discarded. since the number of relevant pixels
    per image may differ, we repeat the last pixel in each column until max(column).
    """
    columns = []
    for (path, _, files) in os.walk('cropped/'):
        files = list(filter(lambda x: '.png' in x, files))
        #files = ['11168_14409217682.png', '11168_14408900002.png', '11168_14408933102.png']
        for im in files:
            image = Image.open('{0}/{1}'.format(path, im))
            arr = np.array(image)
            alpha = arr[:,:,3].ravel()
            rgb = arr[:,:,0:3].ravel()
            mask = np.concatenate((alpha, alpha, alpha))  # once for each color channel
            pixels = rgb[mask == 255] # only use pixels that are visible (alpha=255)
            columns.append(pixels)
        columns = normalize_columns(columns)
        matrix = np.column_stack(columns).T
        return files, matrix
#print(matrix.shape)


def cluster_it(k, matrix):
    k_means = cluster.KMeans(K)
    k_means.fit(matrix)
    return k_means.predict(matrix)  #k_means.labels_


def merge_result(k, labels, files):
    images_per_label = {}
    for i in range(0, k):
        images_per_label[i] = []
    for i,l in enumerate(labels):
        images_per_label[l].append(files[i])
    return images_per_label


def copy_images(images_per_label, empty_dir=True):
    if empty_dir:
        if os.path.exists('clustered/'):
            shutil.rmtree('clustered/')
        os.mkdir('clustered/')
    for k in images_per_label.keys():
        dirname = 'clustered/{0}'.format(str(k))
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        for im in images_per_label[k]:
            shutil.copy('images/{0}'.format(im.replace('png', 'jpg')), dirname)


if __name__ == '__main__':
    files, matrix = build_matrix()
    labels = cluster_it(K, matrix)
    images_per_label = merge_result(K, labels, files)
    #print(images_per_label)
    copy_images(images_per_label)

