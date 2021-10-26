import os
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


def main(path: str):
    pix = Image.open(os.path.join(path, 'input.jpg'))
    e = ImageEnhance.Contrast(pix)
    e.enhance(8.0).filter(ImageFilter.EDGE_ENHANCE).save('edge_enhance.jpg')
    ac = ImageEnhance.Contrast(ImageOps.autocontrast(pix))
    ac.enhance(2.5).save('auto_contrast_enhance.jpg')


if __name__ == '__main__':
    main()
