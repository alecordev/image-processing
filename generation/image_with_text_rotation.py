from PIL import Image, ImageFont, ImageDraw, ImageOps


def main():
    image_width = 350
    image_height = 70
    img = Image.new('RGB', (image_width, image_height), color=(51, 144, 255))

    f = ImageFont.load_default()
    txt = Image.new('L', (500, 50))
    d = ImageDraw.Draw(txt)
    d.text((0, 0), "Someplace Near Boulder", font=f, fill=255)
    w = txt.rotate(17.5, expand=1)

    img.paste(ImageOps.colorize(w, (0, 0, 0), (255, 255, 84)), (242, 60), w)
    img.show()


def f1():
    text = 'Text rotation'
    font = ImageFont.truetype('arial', 50)
    width, height = font.getsize(text)

    image1 = Image.new('RGBA', (200, 150), (0, 128, 0, 92))
    draw1 = ImageDraw.Draw(image1)
    draw1.text((0, 0), text=text, font=font, fill=(255, 128, 0))

    image2 = Image.new('RGBA', (width, height), (0, 0, 128, 92))
    draw2 = ImageDraw.Draw(image2)
    draw2.text((0, 0), text=text, font=font, fill=(0, 255, 128))

    image2 = image2.rotate(30, expand=1)

    px, py = 10, 10
    sx, sy = image2.size
    image1.paste(image2, (px, py, px + sx, py + sy), image2)

    image1.show()


def f2():
    im = Image.new("RGB", (100, 100))
    draw = ImageDraw.Draw(im)
    draw.text((50, 50), "hey")
    im.rotate(45).show()


def f3():
    canvas = Image.new('RGB', (700, 700), color='white')
    fnt = ImageFont.truetype("arial", 36)
    d = ImageDraw.Draw(canvas)
    # d.text((740, 430), 'Rotated message', font=fnt, fill=('#1f6992'))
    d.text((740, 430), 'Rotated message', font=fnt, fill='black')
    canvas.rotate(45, expand=1)
    canvas.show()
    # canvas.save("file2.png", "PNG")


if __name__ == '__main__':
    f3()
