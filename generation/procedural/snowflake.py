from PIL import Image, ImageDraw
import math

def draw_branch(draw, x, y, length, angle, depth, max_depth, width=1):
    """
    Draws a single branch of the snowflake-like tree.

    Args:
        draw (ImageDraw.Draw): The drawing context.
        x, y (float): Starting coordinates of the branch.
        length (float): Length of the branch.
        angle (float): Angle of the branch in radians.
        depth (int): Current recursion depth.
        max_depth (int): Maximum recursion depth.
        width (int): Line width of the branch.
    """
    # Calculate the end point of the branch
    end_x = x + length * math.cos(angle)
    end_y = y + length * math.sin(angle)
    
    # Draw the branch
    draw.line([(x, y), (end_x, end_y)], fill=(255, 255, 255, 255), width=width)
    
    # If the maximum depth is reached, return
    if depth >= max_depth:
        return

    # Recursively draw smaller branches
    new_length = length * 0.6  # Reduce branch length for next level
    draw_branch(draw, end_x, end_y, new_length, angle - math.pi / 6, depth + 1, max_depth, width=max(1, width - 1))
    draw_branch(draw, end_x, end_y, new_length, angle + math.pi / 6, depth + 1, max_depth, width=max(1, width - 1))


def generate_snowflake_tree(output_path="snowflake_tree.png", width=500, height=500, max_depth=6):
    """
    Generate a procedural snowflake-like tree structure.

    Args:
        output_path (str): Path to save the generated image.
        width (int): Width of the image in pixels.
        height (int): Height of the image in pixels.
        max_depth (int): Maximum recursion depth for the tree.
    """
    # Create an image with RGBA mode and transparent background
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(img)
    
    # Start the tree in the center
    center_x = width // 2
    center_y = height // 2
    
    # Draw branches in 6 directions (like a snowflake)
    for i in range(6):
        angle = i * math.pi / 3  # 60-degree increments
        draw_branch(draw, center_x, center_y, length=100, angle=angle, depth=0, max_depth=max_depth)
    
    # Save the generated image
    img.save(output_path, "PNG")
    print(f"Snowflake-like tree saved at: {output_path}")

# Example usage
generate_snowflake_tree(output_path="snowflake_tree.png")
