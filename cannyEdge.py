'''
  File name: cannyEdge.py
  Author: Haoyuan(Steve) Zhang
  Date created: 9/10/2017
'''

'''
  File clarification:
    Canny edge detector 
    - Input: A color image I = uint8(H, W, 3), where H, W are two dimensions of the image
    - Output: An edge map E = logical(H, W)

    - TO DO: Complete three main functions findDerivatives, nonMaxSup and edgeLink 
             to make your own canny edge detector work
'''

import numpy as np
import matplotlib.pyplot as plt
import os, time
from scipy import signal
from PIL import Image

# import functions
from findDerivatives import findDerivatives
from nonMaxSup import nonMaxSup
from edgeLink import edgeLink
from Test_script import Test_script
import utils, helpers


# cannyEdge detector
def cannyEdge(I, fname = None):
  # convert RGB image to gray color space
  T0 = time.time()
  im_gray = utils.rgb2gray(I)

  Mag, Magx, Magy, Ori = findDerivatives(im_gray)
  print(filename, "(findDerivatives) elapsed time:", time.time() - T0)
  # print(Mag.shape,Magx.shape,Magy.shape,Ori.shape)
  M = nonMaxSup(Mag, Ori)
  print(filename, "(nonMaxSup) elapsed time:", time.time() - T0)
  E = edgeLink(M, Mag, Ori)
  print(filename, "(edgeLink) elapsed time:", time.time() - T0)


  # Test_script(im_gray, E)
  # only when test passed that can show all results
  if Test_script(im_gray, E):
    # visualization results
    utils.visDerivatives(im_gray, Mag, Magx, Magy, fname)
    utils.visCannyEdge(I, M, E, fname )

    # plt.show()
  print(filename, "(Test_script) elapsed time:", time.time() - T0)

  return E


if __name__ == "__main__":
  # the folder name that stores all images
  # please make sure that this file has the same directory as image folder
  folder = '../canny_dataset/'

  # read images one by one
  for filename in os.listdir(folder):
    if ".jpg" == filename[-4:]:# and  'I1.jpg'== filename:
      # read in image and convert color space for better visualization
      im_path = os.path.join(folder, filename)
      I = None
      try:
        I = np.array(Image.open(im_path).convert('RGB'))
      except:
        print("cannot open file: ",im_path)

      ## TO DO: Complete 'cannyEdge' function
      if I is not None:
        E = cannyEdge(I, fname = filename[:-4])
    



