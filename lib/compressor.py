import numpy as np
from PIL import Image

from lib.dct import dct
from lib.run_length_encoding import run_length_encoding
from lib.zigzag import zigzag
from src.constants import QUANTI_TABLE, SIZE_BLOCK
from src.helpers import display_rgb, display_ycbcr, pad, rgb2ycbcr, split_rgb


def compress(input_file, output_file, args, logger):
    """Compress the input file and save it to the output file"""
    if args.debug:
        logger.debug("compress " + input_file + " to " + output_file)

    # open image
    try:
        logger.debug("open image")
        img = Image.open(input_file)
    except:
        logger.error("Cannot open " + input_file)
        return

    options = {
        "show": False,
        "save": True,
        "output_file": output_file,
        "img": img
    }

    # get image size
    width, height = img.size
    logger.debug("image size: " + str(width) + "x" + str(height))

    logger.debug("split rgb channels")
    r, g, b = split_rgb(img)

    display_rgb(r, g, b, options)

    logger.debug("convert into Y, Cb, Cr")
    y, Cb, Cr = rgb2ycbcr(r, g, b)

    display_ycbcr(y, Cb, Cr, options)

    logger.debug("downsample Cb and Cr channels")
    Cb = Cb[::2, ::2]
    Cr = Cr[::2, ::2]

    display_ycbcr(y, Cb, Cr, options, ext="downsampled")

    logger.debug("compute DCT for each channel")
    for channel in [y, Cb, Cr]:
        logger.debug("pad channel to be a multiple of " + str(SIZE_BLOCK))
        channel = pad(channel, SIZE_BLOCK)
        # divide into SIZE_BLOCKxSIZE_BLOCK blocks
        for i in range(0, height, SIZE_BLOCK):
            for j in range(0, width, SIZE_BLOCK):
                block = channel[i:i+SIZE_BLOCK, j:j+SIZE_BLOCK]
                # for each block, compute the DCT coefficients matrix
                dct_mat = dct(block)
                # quantize the matrix with a quantization table
                quantized = np.round(dct_mat / QUANTI_TABLE).astype(int)
                # vectorize the matrix in zigzag
                vector = zigzag(quantized)
                # run length encoding on this vector
                rle = run_length_encoding(vector)
