# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pillow"
# ]
# ///

from PIL import Image, ImageDraw, ImageFont

# Load image
image_path = 'input.jpeg'  # Update with your image file
output_path = 'output.jpg'

image = Image.open(image_path).convert("RGBA")
txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
draw = ImageDraw.Draw(txt_layer)

# Text and font
text = "Week 1\n\nSession 1"
font_size = 300
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font = ImageFont.truetype(font_path, font_size)

# Image dimensions
img_w, img_h = image.size

# Background rectangle dimensions (full width, 3/5 height, vertically centered)
rect_h = (3 * img_h) // 5
rect_y0 = (img_h - rect_h) // 2
rect_y1 = rect_y0 + rect_h

# Draw background rectangle (semi-transparent black)
draw.rectangle(
    [(0, rect_y0), (img_w, rect_y1)],
    fill=(0, 0, 0, 180)
)

# Get text size
text_bbox = draw.multiline_textbbox((0, 0), text, font=font)
text_w = text_bbox[2] - text_bbox[0]
text_h = text_bbox[3] - text_bbox[1]
text_x = (img_w - text_w) // 2
text_y = (rect_y0 + rect_y1 - text_h) // 2  # center text within rectangle

# Draw the text
draw.multiline_text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255), align="center")

# Save image
combined = Image.alpha_composite(image, txt_layer)
combined.convert("RGB").save(output_path)

print(f"Saved image with centered overlay to {output_path}")
