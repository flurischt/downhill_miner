"""
fetch all images using the filenames in images/wiriehorn_20150830.json
"""
import json
import requests

URL = 'https://www.webcam-4insiders.com/pictures/original/{0}/Wetter-Webcam-Diemtigen-(Wiriehorn)-{1}'


def down_them_all():
    images = json.load(open('images/wiriehorn_20150830.json', 'r'))
    for im in images:
        (directory, filename) = im.split('/webcam-')
        url = URL.format(directory, filename)
        res = requests.get(url)
        if res.status_code == 200:
            with open('images/{0}'.format(filename), 'wb') as f:
                f.write(res.content)
        else:
            print('{0} failed'.format(im))


if __name__ == '__main__':
    down_them_all()

