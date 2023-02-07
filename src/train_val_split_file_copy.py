import os
import random
import shutil

train_split = 0.8

base_dir = 'D:/Google Drive/FH/COV/dalle_inpainting_classification/'

# 'real_background/'
# 'real_wolf/'
# 'dalle_wolf_inpainting/'
# 'real_background_augment_and_origin/'
# 'real_wolf_augment_and_origin/'
# 'dalle_wolf_inpainting_augment_and_origin/'

img_sources = base_dir + 'images/'
sources_class1 = [img_sources + 'real_wolf_augment_and_origin/']
sources_class2 = [img_sources + 'dalle_wolf_inpainting_augment_and_origin/']
sources_class3 = [img_sources + 'real_background_augment_and_origin/']

img_dest = base_dir + 'image_source/'
dest_class1_train = img_dest + 'train/real_wolf/'
dest_class1_val = img_dest + 'val/real_wolf/'
dest_class2_train = img_dest + 'train/dalle_wolf/'
dest_class2_val = img_dest + 'val/dalle_wolf/'
dest_class3_train = img_dest + 'train/background/'
dest_class3_val = img_dest + 'val/background/'

for d in [dest_class1_train,
          dest_class1_val,
          dest_class2_train,
          dest_class2_val,
          dest_class3_train,
          dest_class3_val]:
    os.makedirs(d)

class1_train = {}
class1_val = {}
for src_cl1 in sources_class1:
    files = os.listdir(src_cl1)
    random.shuffle(files)
    class1_train[src_cl1] = files[:int(len(files) * train_split)]
    class1_val[src_cl1] = files[int(len(files) * train_split):]

class2_train = {}
class2_val = {}
for src_cl2 in sources_class2:
    files = os.listdir(src_cl2)
    random.shuffle(files)
    class2_train[src_cl2] = files[:int(len(files) * train_split)]
    class2_val[src_cl2] = files[int(len(files) * train_split):]

class3_train = {}
class3_val = {}
for src_cl3 in sources_class3:
    files = os.listdir(src_cl3)
    random.shuffle(files)
    class3_train[src_cl3] = files[:int(len(files) * train_split)]
    class3_val[src_cl3] = files[int(len(files) * train_split):]

mapping = {
    dest_class1_train: class1_train,
    dest_class1_val: class1_val,
    dest_class2_train: class2_train,
    dest_class2_val: class2_val,
    dest_class3_train: class3_train,
    dest_class3_val: class3_val,
}

for dest, filemap in mapping.items():
    for src, files in filemap.items():
        for f in files:
            shutil.copy(os.path.join(src, f), dest)
