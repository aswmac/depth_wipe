# file hist.py
# take the component in the given direction
# then scale to range 0..255 and look at the histogram

import cv2
import numpy as np
import math # for sqrt

inputpng = 'your.png' #

#wc = [210, 50, 56]
wc = [0, 43, 185]
wcn = [wc[i]*wc[i] for i in range(3)]
norm2 = sum(wcn)
norm = math.sqrt(norm2)

w = [wc[i]/norm for i in range(3)]

#w = [0.6026, 0.5745, 0.5538] # or any with capturing gray for the image





img = cv2.imread(inputpng)
(width, height, dim) = img.shape
print("shape", width, height, dim)

gimg = np.dot(img[..., :3], w)
g_img = np.floor((gimg - gimg.min())/(gimg.max() - gimg.min())*255 + 0.5)

hist = {}
for i in range(width):
  for j in range(height):
    value = g_img[i][j]
    if value in hist.keys():
      hist[value] += 1
    else:
      hist[value] = 1

N = len(hist)
print("len(hist) = ", N)
print(sorted(hist.keys()))
