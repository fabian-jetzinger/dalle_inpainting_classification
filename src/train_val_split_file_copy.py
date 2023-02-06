import os
import random
import shutil

train_split = 0.8

base_dir = 'D:/Google Drive/FH/COV/dalle_inpainting_classification/'

# '/images/real_background'
# '/images/real_wolf'
# '/images/dalle_wolf_inpainting'

img_sources = base_dir + 'images/'
source_backgrounds = img_sources + 'real_background/'
source_wolves = img_sources + 'dalle_wolf_inpainting'

img_dest = base_dir + 'image_source/'
dest_background_train = img_dest + 'train/background/'
dest_background_val = img_dest + 'val/background/'
dest_wolf_train = img_dest + 'train/wolf/'
dest_wolf_val = img_dest + 'val/wolf/'

for d in [dest_background_train,
          dest_background_val,
          dest_wolf_train,
          dest_wolf_val]:
    os.makedirs(d)

backgrounds = os.listdir(source_backgrounds)
wolves = os.listdir(source_wolves)
random.shuffle(backgrounds)
random.shuffle(wolves)

backgrounds_train = backgrounds[:int(len(backgrounds) * train_split)]
backgrounds_val = backgrounds[int(len(backgrounds) * train_split):]
wolves_train = wolves[:int(len(wolves) * train_split)]
wolves_val = wolves[int(len(wolves) * train_split):]

mapping = {
    dest_background_train: (source_backgrounds, backgrounds_train),
    dest_background_val: (source_backgrounds, backgrounds_val),
    dest_wolf_train: (source_wolves, wolves_train),
    dest_wolf_val: (source_wolves, wolves_val),
}

for dest, tup in mapping.items():
    src, files = tup
    for f in files:
        shutil.copy(os.path.join(src, f), dest)
