def pad(img: np.ndarray, padding: int):
    h, w = img.shape
    h_pad = padding - (h % padding)
    w_pad = padding - (w % padding)
    padded_img = np.pad(img, ((0, h_pad), (0, w_pad)), 'constant')
    return padded_img