import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def replace_extension(path: str, new_extension: str) -> str:
    """Replace the extension of a file"""
    return os.path.splitext(path)[0] + new_extension


def is_image(path: str) -> bool:
    """Check if the file is an image"""
    return path.endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif", ".webp", ".CR2"))


def join(iterator, seperator):
    """Join an iterator with a seperator"""
    it = map(str, iterator)
    seperator = str(seperator)
    string = next(it, '')
    for s in it:
        string += seperator + s
    return string


def fn_without_ext(path: str) -> str:
    """Get the file name without extension"""
    return os.path.splitext(os.path.basename(path))[0]


def rgb2ycbcr(r: np.ndarray, g: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Convert RGB to YCbCr"""
    y = 0.299 * r + 0.587 * g + 0.114 * b
    Cb = -0.1687 * r - 0.3313 * g + 0.5 * b + 128
    Cr = 0.5 * r - 0.4187 * g - 0.0813 * b + 128
    return y, Cb, Cr


class Displayable:
    data: np.ndarray
    cmap: str
    name: str

    def __init__(self, data: np.ndarray = None, cmap: str = None, name: str = None, ext: str = None):
        self.data = data
        self.cmap = cmap
        if ext is not None:
            self.name = name + "_" + ext
        else:
            self.name = name


def display(disps, options):
    """Display the image, and 3 channels"""
    # add options["igm"] at the begining of the disps list
    if options["img"] is not None:
        disps.insert(0, Displayable(options["img"], None, "Original"))

    n = len(disps)

    if options["show"]:
        # find the number of subplots
        nb_rows = int(np.ceil(np.sqrt(n)))
        nb_cols = int(np.ceil(n / nb_rows))

        # create the figure
        _, axs = plt.subplots(nb_rows, nb_cols, figsize=(10, 10))
        axs = axs.flatten()

        # display each subplot
        for i in range(n):
            disp = disps[i]
            axs[i].imshow(disp.data, cmap=disp.cmap)
            axs[i].set_title(disp.name + " channel")
            axs[i].axis('off')

        plt.show()

    if options["save"]:
        output_file = options["output_file"]
        # get file name without extension
        output_filename = fn_without_ext(output_file)
        out_path = os.path.dirname(output_file) + "/" + output_filename + "/"
        if not os.path.exists(out_path):
            os.makedirs(out_path)

        # save each subplot to a file
        for i in range(n):
            disp = disps[i]
            if disp.data is not None:
                if disp.cmap is not None:
                    plt.imsave(
                        out_path + disp.name + ".png",
                        disp.data, cmap=disp.cmap
                    )


def display_rgb(r, g, b, options):
    """Display the image, and 3 channels"""
    r = Displayable(r, "Reds", "red")
    g = Displayable(g, "Greens", "green")
    b = Displayable(b, "Blues", "blue")

    display([r, g, b], options)


def display_ycbcr(y, cb, cr, options, ext=None):
    """Display the image, and 3 channels"""
    y = Displayable(y, "gray", "Y", ext)
    cb = Displayable(cb, "gray", "Cb", ext)
    cr = Displayable(cr, "gray", "Cr", ext)

    display([y, cb, cr], options)


def split_rgb(img) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Split the image into 3 channels"""
    imgs = img.split()
    # convert into numpy array
    r = np.array(imgs[0])
    g = np.array(imgs[1])
    b = np.array(imgs[2])

    return r, g, b


def pad(img: np.ndarray, padding: int) -> np.ndarray:
    """Pad the image with zeros to be a multiple of padding"""
    # get the shape of the image
    h, w = img.shape

    # calculate the padding
    h_pad = padding - (h % padding)
    w_pad = padding - (w % padding)

    # pad the image
    padded_img = np.pad(img, ((0, h_pad), (0, w_pad)), 'constant')

    return padded_img


def log(data, name, i, j, logger, options):
    """Log a message"""
    if options["debug"]:
        if (i == 0 and j == 0):
            if (isinstance(data, list)):
                msg = "\n\t" + name + ":\n"
                msg += "\tShape: " + str(len(data)) + "\n"
                # show the first 10 elements
                msg += "\tData: " + str(data[:10])
            else:
                msg = "Data: " + str(data) + "\n"
            logger.debug(msg)
