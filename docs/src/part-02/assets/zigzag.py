def zigzag(matrix):
    vector = []
    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            if i % 2 == 0:
                vector.append(matrix[i, j])
            else:
                vector.append(matrix[i, matrix.shape[1] - j - 1])
    return vector