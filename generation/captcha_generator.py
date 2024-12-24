import random
import string

from PIL import Image, ImageDraw, ImageFont


class SimpleCaptchaException(Exception):
    pass


class SimpleCaptcha:
    def __init__(
        self,
        length=5,
        size=(200, 100),
        fontsize=36,
        random_text=False,
        random_bgcolor=False,
    ):
        self.size = size
        self.text = "CAPTCHA"
        self.fontsize = fontsize
        self.bgcolor = (255, 255, 255)
        self.length = length
        self.image = None

        if random_text:
            self.text = self._random_text()

        if not self.text:
            raise SimpleCaptchaException("Field text must not be empty.")

        if not self.size:
            raise SimpleCaptchaException("Size must not be empty.")

        if not self.fontsize:
            raise SimpleCaptchaException("Font size must be defined.")

        if random_bgcolor:
            self.bgcolor = self._random_color()

    def _center_coords(self, draw, font):
        # Use `textbbox` instead of `textsize` to get the bounding box of the text
        text_bbox = draw.textbbox((0, 0), self.text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        xy = ((self.size[0] - text_width) / 2, (self.size[1] - text_height) / 2)
        return xy

    def _add_noise_dots(self, draw):
        for _ in range(int(self.size[0] * self.size[1] * 0.1)):
            x = random.randint(0, self.size[0] - 1)
            y = random.randint(0, self.size[1] - 1)
            draw.point((x, y), fill=self._random_color())
        return draw

    def _add_noise_lines(self, draw):
        for _ in range(8):
            width = random.randint(1, 2)
            start = (
                random.randint(0, self.size[0] - 1),
                random.randint(0, self.size[1] - 1),
            )
            end = (
                random.randint(0, self.size[0] - 1),
                random.randint(0, self.size[1] - 1),
            )
            draw.line([start, end], fill=self._random_color(), width=width)
        return draw

    def get_captcha(self, size=None, text=None, bgcolor=None):
        if text is not None:
            self.text = text
        if size is not None:
            self.size = size
        if bgcolor is not None:
            self.bgcolor = bgcolor

        self.image = Image.new("RGB", self.size, self.bgcolor)

        try:
            font = ImageFont.truetype("arial.ttf", self.fontsize)
        except IOError:
            raise SimpleCaptchaException(
                "Font file not found. Please provide a valid path."
            )

        draw = ImageDraw.Draw(self.image)

        xy = self._center_coords(draw, font)
        draw.text(xy, self.text, font=font, fill=self._random_color())

        self._add_noise_dots(draw)
        self._add_noise_lines(draw)
        self.image.save("captcha.jpg")
        return self.image, self.text

    def _random_text(self):
        letters = string.ascii_letters
        return "".join(random.choices(letters, k=self.length))

    def _random_color(self):
        return tuple(random.randint(0, 255) for _ in range(3))


if __name__ == "__main__":
    sc = SimpleCaptcha(length=7, fontsize=36, random_text=True, random_bgcolor=True)
    image, text = sc.get_captcha()
    print(f"Generated CAPTCHA text: {text}")
    image.show()
