import os
from PIL import Image


def main():
    image_file = 'source.jpg'

    img = Image.open(image_file)

    print(img.size)
    print(img._getexif())
    print(img.filename)
    print(img.histogram())
    # plt.hist(img.histogram(), bins=100)
    # plt.show()

    # Size in bytes
    print(os.path.getsize(image_file))
    print(os.stat(image_file).st_size)

    width_original, height_original = img.size
    resize_factor = 0.8  # 1 = keep same size, 0.5 = half size
    new_width = int(width_original * resize_factor)
    new_height = int(height_original * resize_factor)

    modified_image = img.resize((new_width, new_height), Image.ANTIALIAS)
    name, extension = os.path.splitext(image_file)

    new_image_file = name + '_modified' + extension
    modified_image.save(new_image_file)

    print(modified_image.size)
    # Size in bytes
    print(os.path.getsize(new_image_file))
    print(os.stat(new_image_file).st_size)

    # import webbrowser
    # webbrowser.open(new_image_filename)


if __name__ == '__main__':
    main()
