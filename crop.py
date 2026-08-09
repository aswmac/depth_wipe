# file crop.py
# trim amounts in pixels off sides of image

from PIL import Image

img_path = "your.png"

# Open the input image
# image2.png the red high res does left, top, rightdiff, bottomediff = 100, 57, 16, 9
with Image.open(img_path) as img:
    # Get image dimensions
    width, height = img.size
    
    # Define crop boundaries
    left = 97 # 97 // depth one needs 97 here to match dimensions for others...
    top = 55 # 60
    right = width - 16 # 16
    bottom = height - 9 # 9
    
    # Crop the image
    cropped_img = img.crop((left, top, right, bottom))
    
    # Save the output
    cropped_img.save("trimmed.png")
