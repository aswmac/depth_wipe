# file filter_with_depth.py
# use input-depth information and a window blend 1-d kernel to transition
# from input file to a color filter version of the input file
# basically a 1-d convolution in time from image to image

from PIL import Image
import numpy as np
import sys

wb = [1, 1.1, 1.3, 1.6, 2, 2.7, 3, 4, 4.2, 4.5, 4.7, 5]

w = [wb[i]/sum(wb) for i in range(len(wb))] # the window convolution kernel
b = len(w) # the window size
N = 256 # the depth size

# just the regular index, repeats the ends if out of bounds
def padded_index(i, length):
  if i < 0:
    return 0
  if i >= length:
    return length - 1
  return i

def weighted_blend(images, weights):
    """
    Blend a list of images using a weighted average.

    Parameters:
        images (list of np.array): List of image arrays, all same shape (H, W, 3), dtype uint8.
        weights (list or np.array): List of non-negative weights that sum to 1.

    Returns:
        np.array: Blended image, same shape and dtype as inputs.
    """
    if len(images) != len(weights):
        raise ValueError(f"Got {len(images)} images but {len(weights)} weights.")
    if not np.isclose(sum(weights), 1.0):
        raise ValueError(f"Weights must sum to 1.0, got {sum(weights)}")
    if any(w < 0 for w in weights):
        raise ValueError("All weights must be non-negative.")

    # Stack and convert to float for safe computation
    img_stack = np.stack([img.astype(np.float32) for img in images], axis=0)  # (N, H, W, 3)
    w_array = np.array(weights, dtype=np.float32).reshape(-1, 1, 1, 1)  # (N, 1, 1, 1)

    # Weighted sum across images (axis=0)
    blended = np.sum(w_array * img_stack, axis=0)

    # Clip and convert back to uint8
    return np.clip(blended, 0, 255).astype(np.uint8)


def process_images(input_file='trimmed.png', filtered_file='trimmed_red.png', depth_file='trimmed_depth.png', output_prefix='partial_'):
    # Open images
    img = Image.open(input_file).convert('RGB')
    
    filtered_img_np = Image.open(filtered_file).convert('RGB')
    
    depth_img = Image.open(depth_file).convert('L')  # grayscale
    

    # Get dimensions (assume all same size)
    width, height = img.size

    # Convert to numpy arrays for efficient pixel access (optional, but faster than per-pixel getpixel)
    import numpy as np
    img_np = np.array(img)
    print(input_file, "dim", img_np.shape)
    filtered_img_np_np = np.array(filtered_img_np)
    print(filtered_file, "dim", filtered_img_np_np.shape)
    depth_np = np.array(depth_img)
    print(depth_file, "dim", depth_np.shape)

    # Iterate over threshold values 0 to 255
    for threshold in range(1 - b, N + b):
        # Create mask: True where depth >= threshold
        result_np = []
        for j in range(b):
          mask = depth_np >= padded_index(threshold + j, N)
          mask_rgb = np.stack([mask]*3, axis=-1)
          result_np.append(np.where(mask_rgb, filtered_img_np_np, img_np))
        #mask = depth_np >= threshold
        # Broadcast mask to 3 channels for RGB
        #mask_rgb = np.stack([mask]*3, axis=-1)

        # Blend: use filtered_img_np where mask is True, else original img
        #result_np = np.where(mask_rgb, filtered_img_np_np, img_np)
        result_w = weighted_blend(result_np, w)

        # Save result
        output_filename = f"{output_prefix}{(N + b - threshold):03d}.png"
        result_img = Image.fromarray(result_w)
        result_img.save(output_filename)
        print(f"Saved {output_filename}")

if __name__ == '__main__':
    process_images()

