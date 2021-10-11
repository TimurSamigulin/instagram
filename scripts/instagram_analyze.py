import logging
import numpy as np
import math
from PIL import Image
from collections import Counter

import matplotlib.pyplot as plt
import seaborn as sns





class InstaAnalyze:

    def __init__(self):
        self.colorfulness_mean = 43.793
        self.colorfulness_std = 8.286
        self.diversity_mean = 2.261
        self.diversity_std = 0.089
        self.harmony_mean = 44.151
        self.harmony_std = 5.758


    def get_metrics(self, profile):
        pass
        #todo get all user image and predict metrics


    def _get_image(self, image_path):
        image = Image.open(image_path, "r")

        pixel_values = self.__get_image_pixel(image)
        pixel_values_hsv = self.__rgb_to_hsv(pixel_values)
        return pixel_values, pixel_values_hsv


    def __get_image_pixel(self, image):
        width, height = image.size
        pixel_values = list(image.getdata())
        if image.mode == "RGB" or image.mode == "HSV":
            channels = 3
        elif image.mode == "L":
            channels = 1
        else:
            print("Unknown mode: %s" % image.mode)
            return None
        pixel_values = np.array(pixel_values).reshape((width, height, channels))
        return pixel_values

    def __rgb_to_hsv(self, rgb):
        # Translated from source of colorsys.rgb_to_hsv
        # r,g,b should be a numpy arrays with values between 0 and 255
        # rgb_to_hsv returns an array of floats between 0.0 and 1.0.
        rgb = rgb.astype('float')
        hsv = np.zeros_like(rgb)
        # in case an RGBA array was passed, just copy the A channel
        hsv[..., 3:] = rgb[..., 3:]
        r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
        maxc = np.max(rgb[..., :3], axis=-1)
        minc = np.min(rgb[..., :3], axis=-1)
        hsv[..., 2] = maxc
        mask = maxc != minc
        hsv[mask, 1] = (maxc - minc)[mask] / maxc[mask]
        rc = np.zeros_like(r)
        gc = np.zeros_like(g)
        bc = np.zeros_like(b)
        rc[mask] = (maxc - r)[mask] / (maxc - minc)[mask]
        gc[mask] = (maxc - g)[mask] / (maxc - minc)[mask]
        bc[mask] = (maxc - b)[mask] / (maxc - minc)[mask]
        hsv[..., 0] = np.select(
            [r == maxc, g == maxc], [bc - gc, 2.0 + rc - bc], default=4.0 + gc - rc)
        hsv[..., 0] = (hsv[..., 0] / 6.0) % 1.0
        return hsv

    def __rgb2hsv(self, image):
        return image.convert('HSV')

    def __check_image_metrics(self, pixel_rbg, pixel_hsv):
        colorfulness, diversity, harmony = self.__get_image_metrics(pixel_rbg, pixel_hsv)
        metrics = {}
        metrics['colorfulness'] = self.__set_metric(colorfulness, self.colorfulness_mean, self.colorfulness_std)
        metrics['diversity'] = self.__set_metric(diversity, self.diversity_mean, self.diversity_std)
        metrics['harmony'] = self.__set_metric(harmony, self.harmony_mean, self.harmony_std)
        return metrics



    def __set_metric(self, metric, mean_metric, std_metric):
        if metric > mean_metric:
            if metric > mean_metric + std_metric:
                return 4
            else:
                return 3
        else:
            if metric < mean_metric - std_metric:
                return 1
            else:
                return 2


    def __get_image_metrics(self, pixels_rgb, pixels_hsv):
        colorfulness = self.__get_colorfulness(pixels_rgb)
        diversity = self.__color_diversity(pixels_rgb)
        harmony = self.__get_image_harmony(pixels_hsv)
        return colorfulness, diversity, harmony


    def __get_colorfulness(self, pixel_values):
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

    def __create_box_matrix(self, epsilon):
        ran = np.arange(0, 256, epsilon)
        print(ran)

    def __count_non_empty_box(self, image, eps):
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

    def __box_counting_deminsions(self, image, eps):
        non_empty = self.__count_non_empty_box(image, eps)
        d_box = np.log2(non_empty)/np.log2(eps)
        return d_box

    def __color_diversity(self, image):
        eps = [8, 16, 32, 64]
        d_bx = []
        for e in eps:
            d_bx.append(self.__box_counting_deminsions(image, eps=e))

        return np.mean(d_bx)

    def __get_image_harmony(self, image_hsv):
        most_color = self.__freq_color(image_hsv)
        if most_color[0] > most_color[1]:
            return most_color[0] - most_color[1]
        else:
            return most_color[1] - most_color[0]

    def __freq_color(self, image_hsv):
        hue = np.around(image_hsv[:, :, 0].flatten() * 360)
        c = Counter(hue)
        most_color = c.most_common(2)
        return (most_color[0][0], most_color[1][0])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)

    analyze = InstaAnalyze()
    image, image_hsv = analyze._get_image('../data/etosurr/profile_pic + .jpg')
    # print(f'colorfulness: {analyze._get_colorfulness(image)}')
    # print(f'Color diversity: {analyze._color_diversity(image)}')



    # print(max(hue))
    # ax = sns.histplot(hue, bins=30, kde=True, color='skyblue')
    # kdeline = ax.lines[0]
    # xs = kdeline.get_xdata()
    # ys = kdeline.get_ydata()
    # print(ys)
    # # f, ax = plt.subplots(figsize=(7, 7))
    # # aa = sns.kdeplot(hue, ax=ax)
    # plt.show()

