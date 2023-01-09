import cv2
import numpy as np


def dct2(block: np.ndarray) -> np.ndarray:
    """Compute the DCT of a nxm block"""
    # get the size of the block
    n, m = block.shape
    # create the DCT matrix
    dct_mat = np.zeros((n, m))
    # compute the DCT
    for u in range(n):
        for v in range(m):
            # compute the sum
            s = 0
            for i in range(n):
                for j in range(m):
                    s += block[i, j] * np.cos(
                        (2 * i + 1) * u * np.pi / (2 * n)
                    ) * np.cos(
                        (2 * j + 1) * v * np.pi / (2 * m)
                    )
            # compute the coefficient
            if u == 0:
                cu = 1 / np.sqrt(n)
            else:
                cu = np.sqrt(2 / n)
            if v == 0:
                cv = 1 / np.sqrt(m)
            else:
                cv = np.sqrt(2 / m)
            dct_mat[u, v] = cu * cv * s

    return dct_mat


def dct(block: np.ndarray) -> np.ndarray:
    return cv2.dct(block.astype(np.float32))


def idct(block: np.ndarray) -> np.ndarray:
    return cv2.idct(block.astype(np.float32))
