'''
  File name: utils.py
  Author: Haoyuan(Steve) Zhang
  Date created: 9/10/2017
'''

'''
  File clarification:
    Utils file that contributes the project  
'''

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

'''
  Derivatives visualzation function
'''
def visDerivatives(I_gray, Mag, Magx, Magy, filename = None):
  fig, (Ax0, Ax1, Ax2, Ax3) = plt.subplots(1, 4, figsize = (20, 8))

  Ax0.imshow(Mag, cmap='gray', interpolation='nearest')
  Ax0.axis('off')
  Ax0.set_title('Gradient Magnitude')

  Ax1.imshow(Magx, cmap='gray', interpolation='nearest')
  Ax1.axis('off')
  Ax1.set_title('Gradient Magnitude (x axis)')
  
  Ax2.imshow(Magy, cmap='gray', interpolation='nearest')
  Ax2.axis('off')
  Ax2.set_title('Gradient Magnitude (y axis)')

  # plot gradient orientation
  Mag_vec = Mag.transpose().reshape(1, Mag.shape[0] * Mag.shape[1]) 
  hist, bin_edge = np.histogram(Mag_vec.transpose(), 100)

  ind_array = np.array(np.where( (np.cumsum(hist).astype(float) / hist.sum()) < 0.95))
  thr = bin_edge[ind_array[0, -1]]

  ind_remove = np.where(np.abs(Mag) < thr)
  Magx[ind_remove] = 0
  Magy[ind_remove] = 0

  X, Y = np.meshgrid(np.arange(0, Mag.shape[1], 1), np.arange(0, Mag.shape[0], 1))

  Ax3.imshow(I_gray, cmap='gray', interpolation='nearest')
  Ax3.axis('off')
  Ax3.set_title('Gradient Orientation')
  
  Q = plt.quiver(X, Y, Magx, Magy)
  qk = plt.quiverkey(Q, 0.9, 0.9, 2, r'$2 \frac{m}{s}$', labelpos='E', coordinates='figure')
  fig.savefig( str(filename)+ '_visDerivatives.png')


'''
  Edge detection result visualization function
'''
def visCannyEdge(Im_raw, M, E, filename = None):
  # plot image
  fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize = (12, 12))

  # plot original image
  ax0.imshow(Im_raw)
  ax0.axis("off")
  ax0.set_title('Raw image')

  # plot edge detection result
  ax1.imshow(M, cmap='gray', interpolation='nearest')
  ax1.axis("off")
  ax1.set_title('Non-Max Suppression Result')

  # plot original image
  ax2.imshow(E, cmap='gray', interpolation='nearest')
  ax2.axis("off") 
  ax2.set_title('Canny Edge Detection')
  fig.savefig( str(filename)+ '_visCannyEdge.png')

'''
  Generate one dimension Gaussian distribution
  - input mu: the mean of pdf
  - input sigma: the standard derivation of pdf
  - input length: the size of pdf
  - output: a row vector represents one dimension Gaussian distribution
'''
def GaussianPDF_1D(mu, sigma, length):
  # create an array
  half_len = length / 2

  if np.remainder(length, 2) == 0:
    ax = np.arange(-half_len, half_len, 1)
  else:
    ax = np.arange(-half_len, half_len + 1, 1)

  ax = ax.reshape([-1, ax.size])
  denominator = sigma * np.sqrt(2 * np.pi)
  nominator = np.exp( -np.square(ax - mu) / (2 * sigma * sigma) )

  return nominator / denominator

'''
  Generate two dimensional Gaussian distribution
  - input mu: the mean of pdf
  - input sigma: the standard derivation of pdf
  - input row: length in row axis
  - input column: length in column axis
  - output: a 2D matrix represents two dimensional Gaussian distribution
'''
def GaussianPDF_2D(mu, sigma, row, col):
  # create row vector as 1D Gaussian pdf
  g_row = GaussianPDF_1D(mu, sigma, row)
  # create column vector as 1D Gaussian pdf
  g_col = GaussianPDF_1D(mu, sigma, col).transpose()

  return signal.convolve2d(g_row, g_col, 'full')

'''
  Convert RGB image to gray one manually
  - Input I_rgb: 3-dimensional rgb image
  - Output I_gray: 2-dimensional grayscale image
'''
def rgb2gray(I_rgb):
  r, g, b = I_rgb[:, :, 0], I_rgb[:, :, 1], I_rgb[:, :, 2]
  I_gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
  return I_gray


def interp2(v, xq, yq):

  if len(xq.shape) == 2 or len(yq.shape) == 2:
    dim_input = 2
    q_h = xq.shape[0]
    q_w = xq.shape[1]
    xq = xq.flatten()
    yq = yq.flatten()

  h = v.shape[0]
  w = v.shape[1]
  if xq.shape != yq.shape:
    raise 'query coordinates Xq Yq should have same shape'


  x_floor = np.floor(xq).astype(np.int32)
  y_floor = np.floor(yq).astype(np.int32)
  x_ceil = np.ceil(xq).astype(np.int32)
  y_ceil = np.ceil(yq).astype(np.int32)

  x_floor[x_floor<0] = 0
  y_floor[y_floor<0] = 0
  x_ceil[x_ceil<0] = 0
  y_ceil[y_ceil<0] = 0

  x_floor[x_floor>=w-1] = w-1
  y_floor[y_floor>=h-1] = h-1
  x_ceil[x_ceil>=w-1] = w-1
  y_ceil[y_ceil>=h-1] = h-1

  v1 = v[y_floor, x_floor]
  v2 = v[y_floor, x_ceil]
  v3 = v[y_ceil, x_floor]
  v4 = v[y_ceil, x_ceil]

  lh = yq - y_floor
  lw = xq - x_floor
  hh = 1 - lh
  hw = 1 - lw

  w1 = hh * hw
  w2 = hh * lw
  w3 = lh * hw
  w4 = lh * lw

  interp_val = v1 * w1 + w2 * v2 + w3 * v3 + w4 * v4

  if dim_input == 2:
    return interp_val.reshape(q_h,q_w)
  return interp_val







