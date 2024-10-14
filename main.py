from PIL import Image, ImageOps
img = Image.open('media/image/1.tif')
img_border = ImageOps.expand(img, border=2, fill='blue')
img_border.save('1_border.tif')