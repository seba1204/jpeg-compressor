from PIL import Image
img = Image.open(input_file)
r, g, b = split_rgb(img)
y, Cb, Cr = rgb2ycbcr(r, g, b)
display_rgb(r, g, b, options)
display_ycbcr(y, Cb, Cr, options)