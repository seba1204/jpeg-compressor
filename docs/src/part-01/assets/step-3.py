 for k in range(3):
    width, height = input[k].shape
    padded = pad(input[k], SIZE_BLOCK)
    w, h = padded.shape
    output = np.zeros((h, w), dtype=int)
    for i in range(0, h, SIZE_BLOCK):
        for j in range(0, w, SIZE_BLOCK):
            block = padded[i:i+SIZE_BLOCK, j:j+SIZE_BLOCK]
            dct_mat = dct(block)