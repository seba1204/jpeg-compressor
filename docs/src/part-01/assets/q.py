def quantization_matrix(ratio: float) -> np.ndarray:
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