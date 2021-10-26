import io
import pathlib

from PIL import Image, ImageDraw, ImageFont

here = pathlib.Path(__file__).parent.absolute()


def main():
    image_width = 350
    image_height = 70
    img = Image.new('RGB', (image_width, image_height), color=(51, 144, 255))

    canvas = ImageDraw.Draw(img)
    font = ImageFont.truetype('../../fonts/Lato-Bold.ttf', size=24)
    text_width, text_height = canvas.textsize('Text in image', font=font)

    print(f"Text width: {text_width}")
    print(f"Text height: {text_height}")

    x_pos = int((image_width - text_width) / 2)
    y_pos = int((image_height - text_height) / 2)

    print(f"X: {x_pos}")
    print(f"Y: {y_pos}")

    canvas.text((x_pos, y_pos), "Text in image", font=font, fill='#FFFFFF')
    img.save(here.joinpath('image_with_text.png'), format="PNG", dpi=(300, 300))


if __name__ == '__main__':
    main()
