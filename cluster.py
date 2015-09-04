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


def build_matrix():
    columns = []
    for (path, _, files) in os.walk('cropped/'):
        #files = ['11168_14409217682.bmp', '11168_14408900002.bmp', '11168_14408933102.bmp']
        for im in files:
            if '.bmp' not in im:
                continue
            image = Image.open('{0}/{1}'.format(path, im)).convert('RGBA')
            arr = np.array(image)
            flatt_arr = arr.ravel()
            columns.append(flatt_arr)
            #vector = np.matrix(flatt_arr)
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
            shutil.copy('images/{0}'.format(im.replace('bmp', 'jpg')), dirname)


if __name__ == '__main__':
    files, matrix = build_matrix()
    labels = cluster_it(K, matrix)
    images_per_label = merge_result(K, labels, files)
    #print(images_per_label)
    copy_images(images_per_label)

