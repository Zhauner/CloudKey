import os
from PIL import Image, ImageStat


def avarage_clr(filename):

    img = Image.open(filename)
    conv = img.convert("RGB")
    mean = ImageStat.Stat(conv).mean

    if len(mean) >= 3:

        color = '{:.0f} {:.0f} {:.0f}'.format(*mean)
        os.remove("fav.png")

        return color.split(' ')

    elif len(mean) == 2:

        color = '{:.0f} {:.0f} 0'.format(*mean)
        os.remove("fav.png")

        return color.split(' ')

    elif len(mean) == 1:

        color = '{:.0f} 0 0'.format(*mean)

        red_color = [int(x) for x in color.split(' ')]

        if red_color[0] < 100:
            red_color[0] = 100
        os.remove("fav.png")

        return red_color
