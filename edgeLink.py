'''
  File name: edgeLink.py
  Author:
  Date created:
'''

'''
  File clarification:
    Use hysteresis to link edges based on high and low magnitude thresholds
    - Input M: H x W logical map after non-max suppression
    - Input Mag: H x W matrix represents the magnitude of gradient
    - Input Ori: H x W matrix represents the orientation of gradient
    - Output E: H x W binary matrix represents the final canny edge detection map
'''
import numpy as np

def edgeLink(M, Mag, Ori):
  # TODO: your code here
  max_ = Mag.max()
  threshold_low = 0.035
  threshold_high = 0.175
  low = threshold_low * max_
  high = threshold_high * max_
  nrow, ncol = M.shape

  strong_map = np.multiply(M, Mag) > high
  weak_map = np.multiply(low <  np.multiply(M, Mag) , np.multiply(M, Mag) <= high)

  max_iter = 100
  max_n_hop = 200
  FLAG_change = True
  iter = 0
  while FLAG_change and iter < max_iter:
    iter += 1
    FLAG_change = False
    x_list, y_list = np.where(weak_map)
    x_list = list(x_list)
    y_list = list(y_list)
    for i, ix in enumerate(x_list):
      iy = y_list[i]
      if 7*np.pi/8 <= (Ori[ix,iy] + np.pi/2) or (Ori[ix,iy] + np.pi/2) < np.pi/8:
        # check horizontal two points
        for n_hop in range(1,max_n_hop):
          if ix > n_hop -1 :
            if strong_map[ix- n_hop , iy]:
              strong_map[ix,iy] = True
              weak_map[ix,iy] = False
              FLAG_change = True
              break
          if ix < nrow - n_hop:
            if strong_map[ix+ n_hop, iy]:
              strong_map[ix,iy] = True
              weak_map[ix,iy] = False
              FLAG_change = True
              break
      elif np.pi/8 <= (Ori[ix,iy] + np.pi/2) < 3*np.pi/8:
        # check upper-left and lower-right points

        for n_hop in range(1,max_n_hop):
          if ix > n_hop-1 and iy < ncol - n_hop :
            if strong_map[ix-n_hop , iy +n_hop ]:
              strong_map[ix,iy] = True
              weak_map[ix,iy] = False
              FLAG_change = True
              break
          if ix < nrow - n_hop and iy > n_hop -1 :
            if strong_map[ix+ n_hop , iy - n_hop ]:
              strong_map[ix,iy] = True
              weak_map[ix,iy] = False
              FLAG_change = True
              break
      elif 3*np.pi/8<= (Ori[ix,iy] + np.pi/2) < 5*np.pi/8:
        # check vertical two points
        for n_hop in range(1,max_n_hop):
          if iy > n_hop - 1:
            if strong_map[ix , iy - n_hop]:
              strong_map[ix,iy] = True
              weak_map[ix,iy] = False
              FLAG_change = True
              break
          if iy < ncol - n_hop:
            if strong_map[ix, iy + n_hop]:
              strong_map[ix,iy] = True
              weak_map[ix,iy] = False
              FLAG_change = True
              break
      elif 5*np.pi/8 <= (Ori[ix,iy] + np.pi/2) < 7*np.pi/8:
        # check upper-right and lower-left points
        for n_hop in range(1,max_n_hop):
          if ix > n_hop -1 and iy > n_hop -1:
            if strong_map[ix- n_hop , iy - n_hop ]:
              strong_map[ix,iy] = True
              weak_map[ix,iy] = False
              FLAG_change = True
              continue
          if ix < nrow - n_hop and iy < ncol - n_hop:
            # print("ncol", ncol, "nrow", nrow,"ix", ix,"iy",iy,"n_hop", n_hop)
            # print("strong_map.shape", strong_map.shape)
            if strong_map[ix+ n_hop , iy + n_hop ]:
              strong_map[ix,iy] = True
              weak_map[ix,iy] = False
              FLAG_change = True
              continue
  print("iter", iter)
  ret = strong_map.astype(int)
  return ret