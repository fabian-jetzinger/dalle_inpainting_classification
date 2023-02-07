# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 10:35:16 2021

@author: p21702
@editor: S2110595001
"""

import numpy as np
import cv2
import random as rand
import math
from rotate_image import crop_around_center, largest_rotated_rect

# base class
# augmentationParameters: the random values to be applied
# configParameters: the possible range


class AugmentationProcessBase:
    def __init__(self, ID, name, augmentationParameters, configParameters):
        self.ID = ID
        self.name = name
        self.augmentationParameters = augmentationParameters
        self.configParameters = configParameters

    def __init__(self, ID, name, configParameters, width, height):
        self.ID = ID
        self.name = name
        self.configParameters = configParameters
        self.augmentationParameters = self.getRandomAugmentationParameters(
            width, height
		)
        self.width = width
        self.height = height

    def reInit(self):
        self.augmentationParameters = self.getRandomAugmentationParameters(
            self.width, self.height
		)

    def augmentImage(self, inImage):
        return None

    def print(self):
        print(self.name + " [" + self.ID + "], params = " + self.parameters)

    # generate the level of variation
    # if image and reference mask and so on need to get transformed, then this
    # random setup is generated once and then utilized
    def getRandomAugmentationParameters(self, width, height):
        return None


# child classes
# Rotate, Translate, Flip
class AffineTransformationAP(AugmentationProcessBase):

    def getRandomAugmentationParameters(self, width, height):
        rangeTx = self.configParameters[1] * width
        rangeTy = self.configParameters[2] * height
        rangeRot = self.configParameters[3]
        Tx = rand.random() * rangeTx - rangeTx/2
        Ty = rand.random() * rangeTy - rangeTy/2
        Rot = rand.random() * rangeRot - rangeRot/2
        return [Tx, Ty, Rot]

    def augmentImage(self, inImage):
        imageFinal = np.copy(inImage)
        Rot = self.augmentationParameters[2]
        Tx = self.augmentationParameters[0]
        Ty = self.augmentationParameters[1]

        height = np.shape(inImage)[0]
        width = np.shape(inImage)[1]

        # horizontal flip
        if rand.random() < 0.5:
            imageFinal = cv2.flip(imageFinal, 1)

        # rotate
        interpMode = self.configParameters[0]
        MRot = cv2.getRotationMatrix2D((width/2.0, height/2.0), Rot, 1)
        imageFinal = cv2.warpAffine(
            imageFinal, MRot, (width, height), flags=interpMode
		)

        # crop
        imageFinal = crop_around_center(
            imageFinal,
            *largest_rotated_rect(
                width,
                height,
                math.radians(Rot)
            )
        )

        # translation
        # 1 is for the matrix normalization
        Mtrans = np.float32([[1, 0, Tx], [0, 1, Ty]])
        imageFinal = cv2.warpAffine(
            imageFinal, Mtrans, (width, height), flags=interpMode
		)

        # crop
        y_nonzero, x_nonzero, _ = np.nonzero(imageFinal)
        lowest_y = np.min(y_nonzero)
        highest_y = np.max(y_nonzero)
        lowest_x = np.min(x_nonzero)
        highest_x = np.max(x_nonzero)
        save_border = 7
        imageFinal = imageFinal[
			lowest_y+save_border:highest_y-save_border,
			lowest_x+save_border:highest_x-save_border
		]
        return imageFinal


# gamma correction
class GammaCorrectionAP(AugmentationProcessBase):

    def getRandomAugmentationParameters(self, width, height):
        gamma_low = self.configParameters[0]
        gamma_high = self.configParameters[1]
        gamma_range = gamma_high - gamma_low
        gamma = gamma_low + rand.random() * gamma_range
        return [gamma]  # gamma

    def augmentImage(self, inImage):
        gamma_to_lose = self.augmentationParameters[0]
        hsvImg = getHSVimage(inImage)
        vChannel = hsvImg[:, :, 2] / 255.0
        vChannel = np.power(vChannel, 1.0 / gamma_to_lose)
        hsvImg[:, :, 2] = vChannel * 255.0
        rgbImg = getRGBimage(hsvImg)
        return rgbImg


# sharpening / blur
class ConvolutionAP(AugmentationProcessBase):
    sharp_kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    def getRandomAugmentationParameters(self, width, height):
        rand_int = rand.random()
        kernel = None
        if rand_int < self.configParameters[0]:
            size = rand.choice([3,5,7,9])
            kernel = np.ones((size,size), np.float32) / 9
        elif rand_int < self.configParameters[1] + self.configParameters[0]:
            kernel = self.sharp_kernel
        return [kernel]

    def augmentImage(self, inImage):
        resultImg = inImage
        # check if a kernel is set
        if self.augmentationParameters[0] is not None:
            resultImg = cv2.filter2D(
                src=inImage, 
                ddepth=-1,
                kernel=self.augmentationParameters[0]
            )
        return resultImg


def getHSVimage(imageRGB) :
   hsv = cv2.cvtColor(imageRGB, cv2.COLOR_BGR2HSV)
   return hsv


def getRGBimage(imageHSV) :
   rgb = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2BGR)
   return rgb