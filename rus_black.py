import os
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw


class Draw:
    _font = [
        ImageFont.truetype(os.path.join(os.path.dirname(__file__), "res/RoadNumbers2.0.ttf"), 105),
        ImageFont.truetype(os.path.join(os.path.dirname(__file__), "res/RoadNumbers2.0.ttf"), 98),
        ImageFont.truetype(os.path.join(os.path.dirname(__file__), "res/RoadNumbers2.0.ttf"), 80)
    ]
    _bg = cv2.resize(cv2.imread(os.path.join(os.path.dirname(__file__), "res/rus_black_lp.png")), (440, 95))

    def __call__(self, plate):
        if len(plate) != 8:
            print("ERROR: Invalid length")
            return None
        fg = self._draw_fg(plate)
        return cv2.cvtColor(cv2.bitwise_or(fg, self._bg), cv2.COLOR_BGR2RGB)

    def _draw_char(self, ch, size, padding_top):
        img = Image.new("RGB", (45, 95), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text(
            (0, padding_top), ch,
            fill=(255, 255, 255),
            font=self._font[size]
        )
        if img.width > 45:
            img = img.resize((45, 95))
        return np.array(img)

    def _draw_fg(self, plate):
        img = np.array(Image.new("RGB", (440, 95), (0, 0, 0)))
        offset = 30

        img[0:95, offset:offset + 45] = self._draw_char(plate[0], 0, 29)
        offset = offset + 48

        img[0:95, offset:offset + 45] = self._draw_char(plate[1], 0, 29)
        offset = offset + 48

        img[0:95, offset:offset + 45] = self._draw_char(plate[2], 0, 29)
        offset = offset + 48

        img[0:95, offset:offset + 45] = self._draw_char(plate[3], 0, 29)
        offset = offset + 60

        img[0:95, offset:offset + 45] = self._draw_char(plate[4], 1, 33)
        offset = offset + 46

        img[0:95, offset:offset + 45] = self._draw_char(plate[5], 1, 33)
        offset = offset + 72
        img[0:95, offset:offset + 45] = self._draw_char(plate[6], 2, 22)
        offset = offset + 37

        img[0:95, offset:offset + 45] = self._draw_char(plate[7], 2, 22)


        return img


if __name__ == "__main__":
    import argparse
    import matplotlib.pyplot as plt

    parser = argparse.ArgumentParser(description="Generate a yellow plate.")
    parser.add_argument("plate", help="license plate number (default: A000AA00)", type=str, nargs="?", default="8394MM76")
    args = parser.parse_args()

    draw = Draw()
    plate = draw(args.plate)
    plt.imshow(plate)
    plt.show()
