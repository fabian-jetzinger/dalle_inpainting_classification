from random import randint
from augmentation_process import *
import cv2
from os import listdir, makedirs
from os.path import isfile, join, exists

image_path = "D:/Google Drive/FH/COV/dalle_inpainting_classification/images"
dalle_path_name = "dalle_wolf_inpainting"
bg_path_name = "real_background"
wolf_path_name = "real_wolf"

augment_path_name = "_augment_and_origin"
augment_image_name = "augment_"
all_paths_names = [dalle_path_name, bg_path_name, wolf_path_name]

# interpolation strategy, transfX, transfY, rotation
config_transformation = [cv2.INTER_LANCZOS4, 0, 0, 25.0]
# gamma low, gamma high
config_gamma = [0.85, 1]
# blur chance, sharpening chance
config_blur_sharp = [0.25, 0.25]

def augment_all():
	for path_name in all_paths_names:
		current_path = join(image_path, path_name)
		save_path = join(image_path, path_name + augment_path_name)

		if not exists(save_path):
			makedirs(save_path)

		augment_one_path(current_path, save_path)

def augment_one_path(path, save_path):
	for file_name in listdir(path):
		file_path = join(path, file_name)
		print("FILE: ", file_path)

		if not isfile(file_path):
			return

		img = cv2.imread(file_path)
		height = img.shape[0]
		width = img.shape[1]

		save_file_path = join(save_path, file_name)
		cv2.imwrite(save_file_path, img)

		# random horizontal flip
		if randint(0, 1):
			img = cv2.flip(img, 1)

		img = AffineTransformationAP(
			1, 'affineTransformation', config_transformation, width, height
		).augmentImage(img)

		img = GammaCorrectionAP(
			2, 'gamma correction', config_gamma, width, height
		).augmentImage(
			img
		)

		img = ConvolutionAP(
			3, 'convolution', config_blur_sharp, width, height
		).augmentImage(
			img
		)

		save_file_path = join(save_path, augment_image_name + file_name)
		cv2.imwrite(save_file_path, img)

if __name__ == "__main__":
	augment_all()
