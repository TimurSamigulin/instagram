import logging
import numpy as np
from PIL import Image
import math

class InstaAnalyze:

    def _get_image(self, image_path):
        image = Image.open(image_path, "r")
        width, height = image.size
        pixel_values = list(image.getdata())
        if image.mode == "RGB":
            channels = 3
        elif image.mode == "L":
            channels = 1
        else:
            print("Unknown mode: %s" % image.mode)
            return None
        pixel_values = np.array(pixel_values).reshape((width, height, channels))
        return pixel_values

    def _get_colorfulness(self, pixel_values):
        pixels = pixel_values.reshape(pixel_values.shape[0] * pixel_values.shape[1], 3)
        rg = []
        yb = []
        for pixel in pixels:
            rg.append(pixel[0] - pixel[2])
            yb.append((pixel[0] + pixel[1])/2 - pixel[2])

        mean_rgyb = np.sqrt(np.square(np.mean(rg)) + np.square(np.mean(yb)))
        std_rgyb = np.sqrt(np.square(np.std(rg)) + np.square(np.std(yb)))
        C = mean_rgyb + 0.3*std_rgyb
        return C

    def _create_box_matrix(self, epsilon):
        ran = np.arange(0, 256, epsilon)
        print(ran)

    def _count_non_empty_box(self, image, eps):
        pixels = image.reshape(image.shape[0] * image.shape[1], image.shape[2])
        unique_colors = set()
        for pixel in pixels:
            pixel = tuple(pixel)
            round_pixel = []
            for color in pixel:
                round_pixel.append(math.floor(color/eps)*eps)
            round_pixel = tuple(round_pixel)
            unique_colors.add(round_pixel)

        return len(unique_colors)

    def _box_counting_deminsions(self, image, eps):
        non_empty = self._count_non_empty_box(image, eps)
        d_box = np.log2(non_empty)/np.log2(eps)
        return d_box


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)

    analyze = InstaAnalyze()
    image = analyze._get_image('../data/ndavidov/2668876199766580469.jpg')
    print(f'colorfulness: {analyze._get_colorfulness(image)}')
    eps = [8,16,32,64]
    d_bx = []
    for e in eps:
        d_bx.append(analyze._box_counting_deminsions(image, eps=e))

    print(np.mean(d_bx))


