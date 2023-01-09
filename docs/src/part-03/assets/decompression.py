for k in range(3):
    for i in range(0, h, SIZE_BLOCK):
        for j in range(0, w, SIZE_BLOCK):
            block = output[i:i+SIZE_BLOCK, j:j+SIZE_BLOCK]
            dequantized = block * quantization_matrix(args.ratio)
            idct_mat = idct(dequantized)
            actual_shape = input[k][i:i+SIZE_BLOCK, j:j+SIZE_BLOCK].shape
            idct_mat = idct_mat[:actual_shape[0], :actual_shape[1]]
            results[k][i:i+SIZE_BLOCK, j:j+SIZE_BLOCK] = idct_mat
y_r, Cb_r, Cr_r = results
Cb_r = np.repeat(np.repeat(Cb_r, 2, axis=0), 2, axis=1)
Cr_r = np.repeat(np.repeat(Cr_r, 2, axis=0), 2, axis=1)
r = y_r + 1.402 * (Cr_r - 128)
g = y_r - 0.34414 * (Cb_r - 128) - 0.71414 * (Cr_r - 128)
b = y_r + 1.772 * (Cb_r - 128)
r = np.clip(r, 0, 255).astype(np.uint8)
g = np.clip(g, 0, 255).astype(np.uint8)
b = np.clip(b, 0, 255).astype(np.uint8)