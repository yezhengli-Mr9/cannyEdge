'''
  File name: findDerivatives.py
  Author:
  Date created:
'''

'''
  File clarification:
    Compute gradient information of the input grayscale image
    - Input I_gray: H x W matrix as image
    - Output Mag: H x W matrix represents the magnitude of derivatives
    - Output Magx: H x W matrix represents the magnitude of derivatives along x-axis
    - Output Magy: H x W matrix represents the magnitude of derivatives along y-axis
    - Output Ori: H x W matrix represents the orientation of derivatives
'''

import numpy as np
from scipy import signal
from utils import GaussianPDF_1D, GaussianPDF_2D
# def findDerivatives(I_gray):
#   # I_gray = np.matrix(I_gray, dtype = np.int16)
#   # # Mag = I_gray
#   # Magx = I_gray[1:,:] - I_gray[:-1,:]
#   # Magy = I_gray[:, 1:] - I_gray[:, :-1]
#   # # Ori  = 
#   # return Mag, Magx, Magy, Ori

#   nrow,ncol = I_gray.shape
#   G = GaussianPDF_2D(0, 1, 5,5) #nrow,ncol
#   dx, dy = np.gradient(G, axis = (1,0))
#   Magx = signal.convolve2d(I_gray,dx,'same')
#   Magy = signal.convolve2d(I_gray,dy,'same')
#   Mag = np.sqrt(Magx*Magx + Magy*Magy);
#   Ori = np.arctan2(Magy, Magx)
#   return Mag, Magx, Magy, Ori


def findDerivatives(I_gray):
    G = GaussianPDF_2D(0, 1, 5, 5)

    dx = np.array([[1, 0, -1],[1, 0, -1],[1, 0, -1]])
    dy = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])

    Gx = signal.convolve2d(G, dx, mode='same')
    Gy = signal.convolve2d(G, dy, mode='same')

    Magx = signal.convolve2d(I_gray, Gx, 'same')
    Magy = signal.convolve2d(I_gray, Gy, 'same')

    Mag = np.sqrt(Magx**2 + Magy**2)
    Ori = np.arctan2(Magy, Magx)

    return Mag, Magx, Magy, Ori