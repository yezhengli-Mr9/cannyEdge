'''
  File name: utils.py
  Author: Haoyuan(Steve) Zhang
  Date created: 9/12/2017
'''
# import os, cv2, scipy
'''
  File clarification:
    Test the canny edge detection output's format including 
    dimension, size and type
    - Input I: raw image
    - Input E: canny edge detection result
'''
#------------
# Berkeley segmentation dataset 
# https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/grouping/resources.html


def Test_script(I, E):
  test_pass = True

  # E should be 2D matrix
  if E.ndim != 2:
    print('ERROR: Incorrect Edge map dimension! \n')
    test_pass = False
  # end if

  # E should have same size with original image
  nr_I, nc_I = I.shape[0], I.shape[1]
  nr_E, nc_E = E.shape[0], E.shape[1]

  if nr_I != nr_E or nc_I != nc_E:
    print('ERROR: Edge map size has changed during operations! \n')
    test_pass = False
  # end if

  # E should be a binary matrix so that element should be either 1 or 0
  numEle = E.size
  numOnes, numZeros = E[E == 1].size, E[E == 0].size

  if numEle != (numOnes + numZeros):
    print('ERROR: Edge map is not binary one! \n')
    test_pass = False
  # end if

  if test_pass:
    print('Test Passed! \n')
  else:
    print('Test Failed! \n')

  return test_pass

# from findDerivatives import findDerivatives
# from nonMaxSup import nonMaxSup
# if __name__ == "__main__":
#   dir_path = "canny_dataset/"
#   filename_list = os.listdir(dir_path)
#   filename_list = list(set(f.split('.')[0] for f in filename_list))
#   for f in filename_set:
#     image_jpg = cv2.imread(os.path.join(dir_path, f+'.jpg'))
#     image_mat = scipy.io.loadmat(os.path.join(dir_path, f+'.mat'))
#     #-------
#     Mag, Magx, Magy, Ori = findDerivatives(image_jpg)
#     edges = nonMaxSup(Mag, Ori)
    





