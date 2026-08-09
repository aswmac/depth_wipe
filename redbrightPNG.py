# redbrightPNG.py

import cv2
import numpy as np
import math

inputpng = 'trimmed.png'
outputpng = 'blue_output.png'

a = 32 # the lowest value to allow on the main color channel (165 best for the red)
b_a = 128 # the maximum variance on the main channel (63 best for the red)
damp = 0.01 # the factor to dampen out of main channel  0.3)

wc = [56, 50, 210] # the main color channel direction BACKWARDS BGR
#wc = [0, 43, 185]
wcn = [wc[i]*wc[i] for i in range(3)]
norm2 = sum(wcn)
norm = math.sqrt(norm2)

w = [wc[i]/norm for i in range(3)] # the main channel unit direction

#w = [0.6026, 0.5745, 0.5538] # or any with capturing gray for the image

img = cv2.imread(inputpng)
#print("original shape", img.shape)

gimg = np.dot(img[..., :3], w) # gimg is the magnitude of the main channel component
main_gray_img = (gimg - gimg.min())/(gimg.max() - gimg.min())*255
main_projected = main_gray_img[..., np.newaxis]*w
diff_img = img - main_projected # img = main_projected + diff_img # the main channel and the rest
(width, height) = main_gray_img.shape
print("shape", width, height)

hist = {}
for i in range(width):
  for j in range(height):
    if main_gray_img[i][j] in hist.keys():
      hist[main_gray_img[i][j]] += 1
    else:
      hist[main_gray_img[i][j]] = 1

N = len(hist)
print("len(hist) = ", N)

m = {} # map sorted to 0...255 (N=256 for palette)
sh = sorted(hist.keys())
for i in range(N):
  m[sh[i]] = i
# RGB == 209-211, 50, 54-58 for sac red or red, 5/21 red, 28/105 red
w_img = np.zeros((width, height,3), dtype = np.uint8)
#w_img = np.floor((29/255)*main_gray_img + 226)
for i in range(width):
  for j in range(height):
    vr = np.floor((b_a/255)*(main_projected[i][j][2] + damp*diff_img[i][j][2]) + a)
    vg = np.floor((b_a/255)*(main_projected[i][j][1] + damp*diff_img[i][j][1]) + a)
    vb = np.floor((b_a/255)*(main_projected[i][j][0] + damp*diff_img[i][j][0]) + a)
    
    w_img[i][j][2] = vr # red brightened
    w_img[i][j][1] = vg
    w_img[i][j][0] = vb

did = cv2.imwrite(outputpng, w_img)
print("did", did)
