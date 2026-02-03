# core/image_enhancer.py
from PIL import Image, ImageFilter

def add_shadow(image: Image.Image, offset=(2, 2), shadow_color=(0, 0, 0, 128), blur_radius=3, border=5):
    """
    Adds a drop shadow to a transparent PIL Image.

    :param image: The input RGBA image.
    :param offset: (x, y) offset of the shadow.
    :param shadow_color: Color of the shadow.
    :param blur_radius: Blur radius for the shadow.
    :param border: Border padding to accommodate the shadow and blur.
    :return: A new image with the shadow.
    """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # The total size of the new image
    total_width = image.width + abs(offset[0]) + 2 * border
    total_height = image.height + abs(offset[1]) + 2 * border
    
    # Create a transparent background
    shadow_image = Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0))
    
    # Create a solid-colored shadow layer from the original image's alpha
    shadow_layer = Image.new('RGBA', image.size, shadow_color)
    
    # Paste the shadow layer onto the transparent background, offset, using the original alpha channel as a mask
    shadow_image.paste(shadow_layer, (border + offset[0], border + offset[1]), image.getchannel('A'))
    
    # Blur the entire shadow image
    shadow_image = shadow_image.filter(ImageFilter.GaussianBlur(blur_radius))
    
    # Paste the original image on top of the shadow
    shadow_image.paste(image, (border, border), image)
    
    return shadow_image
