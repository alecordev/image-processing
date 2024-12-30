import pathlib
from PIL import Image, ImageDraw, ImageFont

class CardGenerator:
    def __init__(
        self,
        width=350,
        height=700,
        card_color=(0, 0, 0),
        font_path=None,
        font_color=(255, 255, 255),
        title_text="Default Title",
        content_text=None,
        image_path=None,
        image_position="top",
        image_margin=0,
        keep_aspect_ratio=True,
        image_ratio=0.4,
    ):
        self.width = width
        self.height = height
        self.card_color = card_color
        self.font_path = font_path or "../fonts/Disney.ttf"
        self.font_color = font_color
        self.title_text = title_text
        self.content_text = content_text
        self.image_path = image_path
        self.image_position = image_position
        self.image_margin = image_margin
        self.keep_aspect_ratio = keep_aspect_ratio
        self.image_ratio = image_ratio
        self.canvas = None
        self.img = None

    def create_card_base(self):
        """Initialize the card with base color."""
        self.img = Image.new("RGB", (self.width, self.height), color=self.card_color)
        self.canvas = ImageDraw.Draw(self.img)

    def load_font(self, size=48):
        """Load the specified font or fall back to default."""
        try:
            return ImageFont.truetype(self.font_path, size)
        except IOError:
            print(f"Font not found at {self.font_path}. Using default font.")
            return ImageFont.load_default()

    def add_image(self):
        """Add an optional image to the card."""
        if not self.image_path:
            return

        image_path = pathlib.Path(self.image_path)
        if not image_path.exists():
            print(f"Image not found at {image_path}. Skipping image addition.")
            return

        top_img = Image.open(image_path).convert("RGB")
        max_width = self.width
        max_height = int(self.height * self.image_ratio)

        if self.keep_aspect_ratio:
            original_width, original_height = top_img.size
            aspect_ratio = original_width / original_height
            if original_width > max_width or original_height > max_height:
                if aspect_ratio > 1:  # Wider than tall
                    new_width = max_width
                    new_height = int(max_width / aspect_ratio)
                else:  # Taller than wide
                    new_height = max_height
                    new_width = int(max_height * aspect_ratio)
            else:
                new_width, new_height = original_width, original_height

            top_img = top_img.resize((new_width, new_height))
        else:
            top_img = top_img.resize((max_width, max_height))

        x_offset = (self.width - top_img.width) // 2
        if self.image_position == "top":
            y_offset = self.image_margin
        else:  # "bottom"
            y_offset = self.height - top_img.height - self.image_margin

        self.img.paste(top_img, (x_offset, y_offset))

    def add_text(self, text, position, font_size):
        """Add text to the card."""
        font = self.load_font(font_size)
        text_bbox = self.canvas.textbbox((0, 0), text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

        if position == "title":
            x_pos = (self.width - text_width) // 2
            y_pos = int(self.height * self.image_ratio + (self.height * 0.2 - text_height) / 2)
        elif position == "content":
            x_pos = (self.width - text_width) // 2
            y_pos = int(self.height * 0.7)
        else:
            raise ValueError("Position must be 'title' or 'content'.")

        self.canvas.text((x_pos, y_pos), text, font=font, fill=self.font_color)

    def save_card(self, output_path="card_output.png"):
        """Save the generated card to a file."""
        output_path = pathlib.Path(output_path)
        self.img.save(output_path, format="PNG", dpi=(300, 300))
        print(f"Card saved at: {output_path}")

    def generate_card(self, output_path="card_output.png"):
        """Generate the card with all elements."""
        self.create_card_base()
        self.add_image()
        if self.title_text:
            self.add_text(self.title_text, "title", font_size=48)
        if self.content_text:
            self.add_text(self.content_text, "content", font_size=32)
        self.save_card(output_path)


if __name__ == "__main__":
    generator = CardGenerator(
        title_text="Hello World!",
        content_text="This is a sample content text.",
        image_path="top_image.jpg",
        image_position="top",
        font_color=(255, 255, 255),
        card_color=(51, 144, 255),
    )
    generator.generate_card("card_with_image_and_text.png")
