import os
import sys
from PIL import Image


class Thumbnailer:
    def __init__(self, src_folder=None):
        self.src_folder = src_folder
        self.ratio = 0.3
        self.thumbnail_folder = "thumbnails"

    def _create_thumbnails_folder(self):
        thumb_path = os.path.join(self.src_folder, self.thumbnail_folder)
        if not os.path.isdir(thumb_path):
            os.makedirs(thumb_path)

    def _build_thumb_path(self, image_path):
        root = os.path.dirname(image_path)
        name, ext = os.path.splitext(os.path.basename(image_path))
        suffix = ".thumbnail"
        return os.path.join(root, self.thumbnail_folder, name + suffix + ext)

    def _load_files(self):
        files = set()
        for each in os.listdir(self.src_folder):
            each = os.path.abspath(self.src_folder + '/' + each)
            if os.path.isfile(each):
                files.add(each)

        return files

    def _thumb_size(self, size):
        return (int(size[0] * self.ratio), int(size[1] * self.ratio))

    def create_thumbnails(self):
        self._create_thumbnails_folder()
        files = self._load_files()

        for each in files:
            print("Processing: " + each)
            try:
                img = Image.open(each)
                thumb_size = self._thumb_size(img.size)
                resized = img.resize(thumb_size, Image.ANTIALIAS)
                savepath = self._build_thumb_path(each)
                resized.save(savepath)
            except IOError as ex:
                print("Error: " + str(ex))


if __name__ == "__main__":
    assert len(sys.argv) == 2
    src_folder = sys.argv[1]

    if not os.path.isdir(src_folder):
        print(f"Error: Path '{src_folder}' does not exits.")
        sys.exit(-1)
    thumbs = Thumbnailer(src_folder)

    # optionally set the name of each thumbnail folder relative to *src_folder*.
    thumbs.thumbnail_folder = "THUMBS"

    # define ratio to resize image to
    # 0.1 means the original image will be resized to 10% of its size
    thumbs.ratio = 0.1

    # will create set of images in temporary folder
    thumbs.create_thumbnails()
