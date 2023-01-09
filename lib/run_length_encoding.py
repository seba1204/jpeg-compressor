def run_length_encoding(vector):
    """Run length encoding on a vector"""
    rle = []
    count = 1
    for i in range(1, len(vector)):
        if vector[i] == vector[i - 1]:
            count += 1
        else:
            rle.append((vector[i - 1], count))
            count = 1
    rle.append((vector[-1], count))
    return rle
