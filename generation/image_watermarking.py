import numpy as np
from PIL import Image
from PIL import ImageFont, ImageDraw


def main():
    # sample dimensions
    pdf_width = 1000
    pdf_height = 1500

    text_to_be_rotated = 'Watermark'
    message_length = len(text_to_be_rotated)

    # load font (tweak ratio based on your particular font)
    font_ratio = 1.5
    diagonal_percentage = 0.5
    diagonal_length = int(np.sqrt((pdf_width ** 2) + (pdf_height ** 2)))
    diagonal_to_use = diagonal_length * diagonal_percentage
    font_size = int(diagonal_to_use / (message_length / font_ratio))
    font = ImageFont.truetype("arial", font_size)
    # font = ImageFont.load_default() # fallback

    image = Image.new('RGBA', (pdf_width, pdf_height), (0, 128, 0, 92))

    # watermark
    opacity = int(256 * 0.5)
    mark_width, mark_height = font.getsize(text_to_be_rotated)
    watermark = Image.new('RGBA', (mark_width, mark_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)
    draw.text((0, 0), text=text_to_be_rotated, font=font, fill=(0, 0, 0, opacity))
    angle = np.degrees(np.arctan(pdf_height / pdf_width))
    watermark = watermark.rotate(angle, expand=1)

    # merge
    wx, wy = watermark.size
    px = int((pdf_width - wx) / 2)
    py = int((pdf_height - wy) / 2)
    image.paste(watermark, (px, py, px + wx, py + wy), watermark)

    image.show()


if __name__ == '__main__':
    main()
