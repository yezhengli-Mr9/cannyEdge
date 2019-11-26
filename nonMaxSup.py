'''
  File name: nonMaxSup.py
  Author:
  Date created:
'''

'''
  File clarification:
    Find local maximum edge pixel using NMS along the line of the gradient
    - Input Mag: H x W matrix represents the magnitude of derivatives
    - Input Ori: H x W matrix represents the orientation of derivatives
    - Output M: H x W binary matrix represents the edge map after non-maximum suppression
'''

from utils import interp2
import numpy as np
import scipy
def nonMaxSup(Mag, Ori):
  # TODO: your code here
  nrow,ncol = Mag.shape
  x_mesh, y_mesh = np.meshgrid(np.arange(ncol), np.arange(nrow))
  x_mesh_interp1 = x_mesh + np.cos(Ori)
  y_mesh_interp1 = y_mesh + np.sin(Ori)
  interp_v1 = interp2(Mag, x_mesh_interp1, y_mesh_interp1)
  x_mesh_interp2 = x_mesh - np.cos(Ori)
  y_mesh_interp2 = y_mesh - np.sin(Ori)
  interp_v2 = interp2(Mag, x_mesh_interp2, y_mesh_interp2)

  ret = Mag >= interp_v1
  ret = np.multiply(ret, Mag >= interp_v2)
  ret = ret.astype(int)
  return ret

  
