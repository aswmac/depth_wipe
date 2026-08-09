from PIL import Image

# === CONFIG ===
first_path = "partial_266.png"
second_path = "partial_268.png"
output_path = "partial_267.png"

img1 = Image.open(first_path)
img2 = Image.open(second_path)

blended = Image.blend(img1, img2, alpha=0.5)

blended.save(output_path)
