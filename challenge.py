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
import cv2,scipy 




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
  print(fname, "(nonMaxSup) elapsed time:", time.time() - T0)
  E = edgeLink(M, Mag, Ori)
  print(fname, "(edgeLink) elapsed time:", time.time() - T0)


  Test_script(im_gray, E)
  # only when test passed that can show all results
  # if Test_script(im_gray, E):
  #   # visualization results
  #   utils.visDerivatives(im_gray, Mag, Magx, Magy, fname)
  #   utils.visCannyEdge(I, M, E, fname )

  #   plt.show()
  print(filename, "(Test_script) elapsed time:", time.time() - T0)

  return E


if __name__ == "__main__":
  # the folder name that stores all images
  # please make sure that this file has the same directory as image folder
  folder = '../challenging_videos/'

  # read images one by one
  for filename in os.listdir(folder):
    if ".mp4" == filename[-4:]:# and  'I1.jpg'== filename:
      # read in image and convert color space for better visualization
      video_path = os.path.join(folder, filename)
      V = None
      try:
        V = cv2.VideoCapture(video_path)
      except:
        print("cannot open file: ", video_path)

      count =0
      ## TO DO: Complete 'cannyEdge' function
      if V is not None:
        video_length = int(V.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        print("Number of frames: ", video_length)
        list_name = []
        while V.isOpened():
            ret, frame = V.read()
            output_filename = "temp/"+filename[:-4]+"_frame{:04d}.jpg".format(count)
            output_filename_complete = os.path.join(folder, output_filename)
            E = cannyEdge(frame, output_filename_complete)
            im = scipy.misc.toimage(E)
            # print(E)
            list_name.append(output_filename_complete)
            # cv2.imwrite(output_filename_complete, E) # , cmap = 'grey', interpolation='nearest'
            im.save(output_filename_complete)
            count += 1
            if (count > (video_length-1)):
              # Release the feed
              V.release()
              # Print stats
              print ("Done extracting frames.\n%d frames extracted" % count)
              # print ("It took %d seconds forconversion." % (time_end-time_start))
              break
            
        

        video_name =  os.path.join(folder, filename[:-4]+'_output.avi')

        frame = cv2.imread(list_name[0])
        height, width, layers = frame.shape

        video = cv2.VideoWriter(video_name, -1, 1, (width,height))

        for image_fname in list_name:
            video.write(cv2.imread(image_fname))

        cv2.destroyAllWindows()
        video.release()
            



