import pathlib
from PIL import Image, ImageDraw, ImageFont

here = pathlib.Path(__file__).parent.absolute()

def main():
    image_width = 350
    image_height = 700
    card_color = (51, 144, 255)
    img = Image.new('RGB', (image_width, image_height), color=card_color)

    canvas = ImageDraw.Draw(img)

    # Define font for text
    font_path = '../fonts/Disney.ttf'
    try:
        font = ImageFont.truetype(font_path, size=48)
    except IOError:
        print(f"Font not found at {font_path}. Using default font.")
        font = ImageFont.load_default()

    # Optional top image
    top_image_path = here.joinpath('top_image.jpg')
    if top_image_path.exists():
        top_img = Image.open(top_image_path).convert("RGB")  # Ensure compatibility with main canvas

        # Calculate aspect-ratio-preserving dimensions
        original_width, original_height = top_img.size
        max_width = image_width
        max_height = int(image_height * 0.4)

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
        
        # Center the top image horizontally
        x_offset = (image_width - new_width) // 2
        img.paste(top_img, (x_offset, 0))

    # Add text to the card
    text = "Text in image"
    text_bbox = canvas.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    x_pos = int((image_width - text_width) / 2)
    y_pos = int(image_height * 0.4 + (image_height * 0.6 - text_height) / 2)  # Position below the top image

    canvas.text((x_pos, y_pos), text, font=font, fill='#FFFFFF')

    # Save the image
    output_path = here.joinpath('card_with_image.png')
    img.save(output_path, format="PNG", dpi=(300, 300))
    print(f"Card saved at: {output_path}")


if __name__ == '__main__':
    main()