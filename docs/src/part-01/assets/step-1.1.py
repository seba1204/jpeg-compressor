def rgb2ycbcr(r, g, b) :
    y = 0.299 * r + 0.587 * g + 0.114 * b
    Cb = -0.1687 * r - 0.3313 * g + 0.5 * b + 128
    Cr = 0.5 * r - 0.4187 * g - 0.0813 * b + 128
    return y, Cb, Cr