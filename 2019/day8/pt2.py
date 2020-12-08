#!/usr/bin/env python

import numpy
from matplotlib.pyplot import imshow, show


def verify(img, width, height):
    layer = 1
    layers = []
    while layer * width * height + 2 < len(img):
        nZeroes = 0
        nOnes = 0
        nTwos = 0
        for n in range(layer * width * height, (layer + 1) * width * height):
            if img[n] == "0":
                nZeroes += 1
            elif img[n] == "1":
                nOnes += 1
            elif img[n] == "2":
                nTwos += 1
        layers.append((nZeroes, nOnes, nTwos))
        layer += 1

    minZeroes = None
    minZeroesLayer = -1
    for layer in range(len(layers)):
        if minZeroes is None or layers[layer][0] < minZeroes:
            minZeroes = layers[layer][0]
            minZeroesLayer = layer

    return layers[minZeroesLayer][1] * layers[minZeroesLayer][2]


def build_image(raw_data, width, height):
    img = numpy.full(height * width, 2)
    for layer in range(len(raw_data) // (width * height)):
        for n in range(layer * width * height, (layer + 1) * width * height):
            if img[n % (width * height)] == 2:
                img[n % (width * height)] = int(raw_data[n])
    return img.reshape(height, width)





if __name__ == "__main__":
    with open("data") as data:
        img = data.read()

    img = build_image(img, 25, 6)
    imshow(img)
    show()
