import io
import pathlib

from PIL import Image


def main():
    here = pathlib.Path(__file__).parent.absolute()

    size = (50, 50)
    img = Image.new('RGB', size, 'black')
    file_object = io.BytesIO()
    img.save(file_object, format='PNG', dpi=(300, 300))  # you could save directly to file here

    with open(here.joinpath('filename.png'), 'wb') as image:
        image.write(file_object.getvalue())


if __name__ == '__main__':
    main()
