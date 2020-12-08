#!/usr/bin/env python

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





if __name__ == "__main__":
    with open("data") as data:
        img = data.read()

    print(verify(img, 25, 6))
