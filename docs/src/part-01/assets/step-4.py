 for k in range(3):
    # ...
    for i in range(0, h, SIZE_BLOCK):
        for j in range(0, w, SIZE_BLOCK):
            # ...
            quantized = np.round( dct_mat / quantization_matrix(args.ratio)).astype(int)
            output[i:i+SIZE_BLOCK, j:j+SIZE_BLOCK] = quantized