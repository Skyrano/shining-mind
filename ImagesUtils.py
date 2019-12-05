import numpy as np     		# multi-dimensional arrays
from PIL import Image  		# images
import matplotlib.pyplot as plt # used to display a matrix as an image

#-------------------------------------------------
# Utility functions for images.
#
# An image is represented as a 3-dimensional array of unsigned
# integers. The 3 dimensions represent:
# - the image columns (size: the image width in pixels)
# - the image lines (size: the image height in pixels)
# - the pixels (3 unsigned integers representing the RGB values)
#-------------------------------------------------

#-------------------------------------------------
# Read an image from a file and return a 3-dimensional array of
# unsigned integers.
#
# input:
#   filename: the name of the image file to be read
#
# output:
#   a 3-dimensional array of unsigned integers representing the image
#-------------------------------------------------
def read_img(filename):
    
    img = np.array(Image.open(filename))
    
    # get a read-only array of the image
    try:
        pixels = np.asarray(img, dtype='uint8')
    except SystemError:
        pixels = np.asarray(img.getdata(), dtype='uint8')

    # make the image writable
    pixels.setflags(write=1)

    return pixels

#-------------------------------------------------
# Convert a 3-dimensional array of integers to an image and write it
# to a file.
#
# input:
#   filename: the name of the file where the image should be written
#   pixels: a 3-dimensional array of unsigned integers representing
#   the image
#-------------------------------------------------
def write_img(filename, pixels):
    img = Image.fromarray(pixels)
    img.save(filename)

#-------------------------------------------------
# Make a 3-dimensional array of integers to represent an image having
# the given dimensions.
#
# input:
#   width: the image width in pixels
#   height: the image height in pixels
#
# output:
#   a 3-dimensional array of unsigned integers a black image (all
#   pixels are zeros)
#-------------------------------------------------
def empty_img(width, height):
    return np.zeros((width, height, 3), dtype='uint8')

#-------------------------------------------------
# Give the width in pixels of an image represented as a 3-dimensional
# array of unsigned integers.
#
# input:
#   pixels: a 3-dimensional array of unsigned integers representing
#   the image
#
# output:
#   width: the image width in pixels
#-------------------------------------------------
def get_width(pixels):
    return np.shape(pixels)[0]

#-------------------------------------------------
# Give the height in pixels of an image represented as a 3-dimensional
# array of unsigned integers.
#
# input:
#   pixels: a 3-dimensional array of unsigned integers representing
#   the image
#
# output:
#   height: the image height in pixels
#-------------------------------------------------
def get_height(pixels):
    return np.shape(pixels)[1]

#-------------------------------------------------
# Display an image represented as a 3-dimensional
# array of unsigned integers.
#
# input:
#   pixels: a 3-dimensional array of unsigned integers representing
#   the image
#
# output:
#   the image displayed
#-------------------------------------------------
def display_img(pixels):
    plt.imshow(pixels)
    return plt.show()


