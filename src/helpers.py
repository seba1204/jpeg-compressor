import cv2
import numpy as np

# open a RAW image
# convert it to YCrCb channels
# downsample Cb and Cr channels
# compute DCT for each channel
#   divide image in 8x8 blocks
#   for each block compute DCT coefficients matrix
#   quantize the matrix with a quantization table


def zigzag(matrix):
    """Convert a matrix in zigzag vector"""
    vector = []
    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            if i % 2 == 0:
                vector.append(matrix[i, j])
            else:
                vector.append(matrix[i, matrix.shape[1] - j - 1])
    return vector


def run_length_encoding(vector):
    """Run length encoding on a vector"""
    rle = []
    count = 1
    for i in range(1, len(vector)):
        if vector[i] == vector[i-1]:
            count += 1
        else:
            rle.append((vector[i-1], count))
            count = 1
    rle.append((vector[-1], count))
    return rle


PATH = "src/lena.png"
QUANTI_TABLE = [
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
]

# open image
i = cv2.imread(PATH)
Y, Cb, Cr = cv2.split(cv2.cvtColor(i, cv2.COLOR_BGR2YUV))   

# downsample Cb and Cr channels
Cb_down = cv2.resize(Cb, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
Cr_down = cv2.resize(Cr, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

# compute DCT for each channel
for channel in [Y, Cb_down, Cr_down]:
    # divide image in 8x8 blocks
    for i in range(0, channel.shape[0], 8):
        for j in range(0, channel.shape[1], 8):
            # for each block compute DCT coefficients matrix
            dct = cv2.dct(channel[i:i+8, j:j+8])
            # quantize the matrix with a quantization table
            channel[i:i+8, j:j+8] = np.round(dct / QUANTI_TABLE)
            # vectorize the matrix in zigzag
            vector = zigzag(channel[i:i+8, j:j+8])
            # run length encoding on this vector
            vector = run_length_encoding(vector)

# merge Y, Cb and Cr channels
