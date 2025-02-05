from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    # Create a new image with a transparent background
    width = 200
    height = 200
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw a circle
    circle_color = (108, 99, 255)  # #6C63FF (primary color)
    circle_bbox = [20, 20, 180, 180]
    draw.ellipse(circle_bbox, fill=circle_color)
    
    # Add text
    try:
        font = ImageFont.truetype('arial.ttf', 60)
    except:
        font = ImageFont.load_default()
    
    # Add "TC" text
    text = "TC"
    text_color = (255, 255, 255)  # White
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    draw.text((x, y), text, font=font, fill=text_color)
    
    # Save the logo
    static_dir = 'together_culture/together_culture_app/static/images'
    os.makedirs(static_dir, exist_ok=True)
    
    # Save full logo
    image.save(os.path.join(static_dir, 'logo.png'))
    
    # Create and save favicon (32x32)
    favicon = image.resize((32, 32), Image.Resampling.LANCZOS)
    favicon.save(os.path.join(static_dir, 'favicon.png'))

if __name__ == '__main__':
    create_logo() 