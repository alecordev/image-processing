"""
Image.resize resizes to the dimensions you specify:

Image.resize([256,512],PIL.Image.ANTIALIAS) # resizes to 256x512 exactly
Image.thumbnail resizes to the largest size that
    (a) preserves the aspect ratio,
    (b) does not exceed the original image, and
    (c) does not exceed the size specified in the arguments of thumbnail.

Image.thumbnail([256, 512],PIL.Image.ANTIALIAS) # resizes 512x512 to 256x256

Furthermore, calling thumbnail resizes it in place, whereas resize returns the resized image.

thumbnail also does not enlarge the image. So e.g. an image of the size 150x150 will keep this dimension if Image.thumbnail([512,512],PIL.Image.ANTIALIAS) is called.
"""
from PIL import Image


def main(filename: str):
    with Image.open(filename) as im:
        im.thumbnail((256, 256))
        im.save(filename.split('.')[0] + '_thumbnail.jpg', "JPEG")


if __name__ == '__main__':
    main("../generation/image_with_text.png")
