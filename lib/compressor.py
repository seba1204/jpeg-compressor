import numpy as np
from PIL import Image

from lib.dct import dct, idct
from lib.run_length_encoding import run_length_encoding
from lib.zigzag import zigzag
from src.constants import QUANTI_TABLE, SIZE_BLOCK
from src.helpers import (display_results, display_rgb, display_ycbcr, pad,
                         rgb2ycbcr, split_rgb)


def quantization_matrix(ratio: float) -> np.ndarray:
    """Compute the quantization matrix"""
    # cf https://www.sciencedirect.com/science/article/pii/S1742287608000285#fd1
    quality = int(100 - ratio * 100)
    if (quality < 50):
        scale = 5000 / quality
    else:
        scale = 200 - 2 * quality

    m = np.zeros((8, 8), dtype=int)

    for i in range(8):
        for j in range(8):
            m[i, j] = int(QUANTI_TABLE[i][j] * scale + 50) / 100

    return m


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
        "debug": args.debug,
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
    # downsample by 2 Cb and Cr by taking only one pixel every 2x2 pixels
    Cb_d = np.zeros((height // 2, width // 2), dtype=int)
    Cr_d = np.zeros((height // 2, width // 2), dtype=int)
    for i in range(0, height, 2):
        for j in range(0, width, 2):
            Cb_d[i // 2, j // 2] = Cb[i, j]
            Cr_d[i // 2, j // 2] = Cr[i, j]

    display_ycbcr(y, Cb_d, Cr_d, options, ext="downsampled")

    logger.debug("compute DCT for each channel")

    input = [y, Cb_d, Cr_d]
    results = [
        np.zeros((height, width), dtype=int),
        np.zeros((height // 2, width // 2), dtype=int),
        np.zeros((height // 2, width // 2), dtype=int)
    ]

    for k in range(len(input)):
        width, height = input[k].shape
        padded = pad(input[k], SIZE_BLOCK)
        w, h = padded.shape
        output = np.zeros((h, w), dtype=int)

        # encode channel

        for i in range(0, h, SIZE_BLOCK):
            for j in range(0, w, SIZE_BLOCK):
                block = padded[i:i+SIZE_BLOCK, j:j+SIZE_BLOCK]
                # for each block, compute the DCT coefficients matrix
                dct_mat = dct(block)
                # quantize the matrix with a quantization table
                quantized = np.round(
                    dct_mat / quantization_matrix(args.ratio)).astype(int)
                output[i:i+SIZE_BLOCK, j:j+SIZE_BLOCK] = quantized

        # decode channel

        for i in range(0, h, SIZE_BLOCK):
            for j in range(0, w, SIZE_BLOCK):
                block = output[i:i+SIZE_BLOCK, j:j+SIZE_BLOCK]
                # dequantize the matrix with a quantization table
                dequantized = block * quantization_matrix(args.ratio)
                # for each block, compute the DCT coefficients matrix
                idct_mat = idct(dequantized)

                # remove padding
                actual_shape = input[k][i:i+SIZE_BLOCK, j:j+SIZE_BLOCK].shape
                idct_mat = idct_mat[:actual_shape[0], :actual_shape[1]]

                results[k][i:i+SIZE_BLOCK, j:j+SIZE_BLOCK] = idct_mat

    y_r, Cb_r, Cr_r = results

    # merge channels
    logger.debug("merge channels")

    # upsample Cb and Cr channels
    Cb_r = np.repeat(np.repeat(Cb_r, 2, axis=0), 2, axis=1)
    Cr_r = np.repeat(np.repeat(Cr_r, 2, axis=0), 2, axis=1)

    # convert into RGB
    r = y_r + 1.402 * (Cr_r - 128)
    g = y_r - 0.34414 * (Cb_r - 128) - 0.71414 * (Cr_r - 128)
    b = y_r + 1.772 * (Cb_r - 128)

    # clip values
    r = np.clip(r, 0, 255).astype(np.uint8)
    g = np.clip(g, 0, 255).astype(np.uint8)
    b = np.clip(b, 0, 255).astype(np.uint8)

    # display image
    display_results(r, g, b, options, "reconstructed")
