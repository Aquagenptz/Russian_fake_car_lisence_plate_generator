import cv2
import random
import numpy as np
import mxnet as mx

import os
import re

import rus_white_short
import rus_white_long
import rus_yellow
import rus_blue
import rus_black
import rus_red_long
import rus_red_short

class Draw:
    _draw = [
        rus_white_short.Draw(),
        rus_white_long.Draw(),
        rus_yellow.Draw(),
        rus_blue.Draw(),
        rus_black.Draw(),
        rus_red_long.Draw(),
        rus_red_short.Draw()
    ]

    _chars_en = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V",
                  "W", "X", "Y", "Z"]
    _chars_dip = ["A", "B", "C", "D", "E", "O", "H", "K", "M", "P", "T", "X", "Y"]
    _chars_rus = ["A", "B", "C", "E", "O", "H", "K", "M", "P", "T", "X", "Y"]
    _digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def __call__(self):
        choice = random.random()

        if choice < 0.83:
            draw = random.choice(self._draw[:2])
        elif choice < 0.99:
            draw = random.choice(self._draw[2:6])
        else:
            draw = random.choice(self._draw[-2:])

        candidates = []
        if type(draw) == rus_white_short.Draw:
            candidates += [self._chars_rus] * 1
            candidates += [self._digits] * 3
            candidates += [self._chars_rus] * 2
            candidates += [self._digits] * 2
            label = "".join([random.choice(c) for c in candidates])
            return draw(label), label
        elif type(draw) == rus_white_long.Draw:
            candidates += [self._chars_rus] * 1
            candidates += [self._digits] * 3
            candidates += [self._chars_rus] * 2
            candidates += [self._digits] * 3
            label = "".join([random.choice(c) for c in candidates])
            return draw(label), label
        elif type(draw) == rus_yellow.Draw:
            candidates += [self._chars_rus] * 2
            candidates += [self._digits] * 5
            label = "".join([random.choice(c) for c in candidates])
            return draw(label), label
        elif type(draw) == rus_blue.Draw:
            candidates += [self._chars_rus] * 1
            candidates += [self._digits] * 6
            label = "".join([random.choice(c) for c in candidates])
            return draw(label), label
        elif type(draw) == rus_black.Draw:
            candidates += [self._digits] * 4
            candidates += [self._chars_rus] * 2
            candidates += [self._digits] * 2
            label = "".join([random.choice(c) for c in candidates])
            return draw(label), label
        elif type(draw) == rus_red_long.Draw:
            candidates += [self._digits] * 3
            candidates += [self._chars_dip] * 1
            candidates += [self._digits] * 5
            label = "".join([random.choice(c) for c in candidates])
            return draw(label), label

        elif type(draw) == rus_red_short.Draw:
            candidates += [self._digits] * 3
            candidates += [self._chars_dip] * 2
            candidates += [self._digits] * 3
            label = "".join([random.choice(c) for c in candidates])
            return draw(label), label


def gauss_blur(image, level):
    return cv2.blur(image, (level * 2 + 1, level * 2 + 1))

def gauss_noise(image):
    for i in range(image.shape[2]):
        c = image[:, :, i]
        diff = 255 - c.max();
        noise = np.random.normal(0, random.randint(1, 6), c.shape)
        noise = (noise - noise.min()) / (noise.max() - noise.min())
        noise = diff * noise
        image[:, :, i] = c + noise.astype(np.uint8)
    return image

def fake_plate(smudge=None):
    draw = Draw()
    plate, label = draw()
    if smudge:
        plate = smudge(plate)
    plate = gauss_blur(plate, random.randint(1, 8))
    plate = gauss_noise(plate)
    return mx.nd.array(plate), label


class Smudginess:
    def __init__(self, smu="res/smu.png"):
        self._smu = cv2.imread(str(smu))

    def __call__(self, raw):
        y = random.randint(0, self._smu.shape[0] - raw.shape[0])
        x = random.randint(0, self._smu.shape[1] - raw.shape[1])
        texture = self._smu[y:y+raw.shape[0], x:x+raw.shape[1]]
        return cv2.bitwise_not(cv2.bitwise_and(cv2.bitwise_not(raw), texture))




if __name__ == "__main__":
    import math
    import argparse
    import matplotlib.pyplot as plt

    parser = argparse.ArgumentParser(description="Generate a random russian car license plate.")
    parser.add_argument("--num", help="set the number of plates (default: 10)", type=int, default=10)
    args = parser.parse_args()

    SAVE_PATH = "rus_random_plate"

    directory_out = f"{os.getcwd()}/{SAVE_PATH}/"

    if not os.path.exists(directory_out):
        os.makedirs(directory_out)  # make new dir

    mud = Smudginess()
    draw = Draw()

    for i in range(args.num):
        plate, label = draw()
        plate = mud(plate)
        plate = gauss_blur(plate, random.randint(1, 8))
        plate = gauss_noise(plate)

        cv2.imwrite(directory_out + label + '.jpg', cv2.cvtColor(plate, cv2.COLOR_RGB2BGR))




