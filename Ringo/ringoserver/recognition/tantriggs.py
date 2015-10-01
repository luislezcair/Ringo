#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Calculates the TanTriggs Preprocessing as described in:
#
#      Tan, X., and Triggs, B. "Enhanced local texture feature sets for face
#      recognition under difficult lighting conditions.". IEEE Transactions
#      on Image Processing 19 (2010), 1635–650.
#
# Default parameters are taken from the paper

import cv2
import numpy as np


ALPHA = 0.1
TAU = 10.0
GAMMA = 0.2
SIGMA0 = 1
SIGMA1 = 2


def tantriggs(image):
    # Convert to float
    image = np.float32(image)

    image = cv2.pow(image, GAMMA)
    image = difference_of_gaussian(image)

    # mean 1
    tmp = cv2.pow(cv2.absdiff(image, 0), ALPHA)
    mean = cv2.mean(tmp)[0]
    image = cv2.divide(image, cv2.pow(mean, 1.0/ALPHA))

    # mean 2
    tmp = cv2.pow(cv2.min(cv2.absdiff(image, 0), TAU), ALPHA)
    mean = cv2.mean(tmp)[0]
    image = cv2.divide(image, cv2.pow(mean, 1.0/ALPHA))

    # tanh
    exp_x = cv2.exp(cv2.divide(image, TAU))
    exp_negx = cv2.exp(cv2.divide(-image, TAU))
    image = cv2.divide(cv2.subtract(exp_x, exp_negx), cv2.add(exp_x, exp_negx))
    image = cv2.multiply(image, TAU)

    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)

    return image


def difference_of_gaussian(image):
    kernel_size0 = SIGMA0 * 3
    kernel_size1 = SIGMA1 * 3

    kernel_size0 += 1 if kernel_size0 % 2 == 0 else 0
    kernel_size1 += 1 if kernel_size1 % 2 == 0 else 0

    gaussian0 = cv2.GaussianBlur(image, (kernel_size0, kernel_size0), SIGMA0, None, SIGMA0, cv2.BORDER_REPLICATE)
    gaussian1 = cv2.GaussianBlur(image, (kernel_size1, kernel_size1), SIGMA1, None, SIGMA1, cv2.BORDER_REPLICATE)

    return cv2.subtract(gaussian0, gaussian1)
