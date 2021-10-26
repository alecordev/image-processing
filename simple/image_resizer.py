import os
import sys

from PIL import Image


def main_dir_worker(d='.'):
    for root, dirs, files in os.walk(d):
        for f in files:
            if f.endswith(".py"):
                print(os.path.join(root, f))  # full path
                print(f)  # the actual name
            if f.endswith(".jpg"):
                process_image(os.path.join(root, f))
                print("jpg")


def process_image(image_file='image.jpg'):
    try:
        img_org = Image.open(image_file)
        # get the size of the original image
        print(img_org.size)
        width_org, height_org = img_org.size

        # set the resizing factor so the aspect ratio can be retained
        # factor > 1.0 increases size
        # factor < 1.0 decreases size
        factor = 1
        width = int(width_org * factor)
        height = int(height_org * factor)

        # best down-sizing filter
        img_anti = img_org.resize((width, height), Image.ANTIALIAS)

        # split image filename into name and extension
        name, ext = os.path.splitext(image_file)

        # create a new file name for saving the result
        new_image_file = "{}{}{}".format(name, str(factor), ext)
        img_anti.save(new_image_file)

        print("\nResized/processed image file saved as {}".format(new_image_file))

        # one way to show the image is to activate
        # the default viewer associated with the image type
        import webbrowser
        webbrowser.open(new_image_file)
    except Exception as e:
        print(f'Error while processing image {image_file}: {e}')
        exit(1)


def usage():
    print('Usage: image_resizer.py <image_file.ext> <new_image_file.ext> (Images can be the same to replace them).')
    print('\nimage_resizer.py dir <MAIN_IMAGE_DIR>: Will work every image in current dir and subdirs')


if __name__ == '__main__':
    print(sys.argv)
    print(len(sys.argv))
    if len(sys.argv) < 3:
        main_dir_worker(r'.')
    else:
        image_file = sys.argv[1]
        new_image_file = sys.argv[2]
