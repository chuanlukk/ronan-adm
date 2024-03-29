import pickle
import numpy as np
import tensorflow as tf
import PIL.Image

import os
from my_utils import create_time_named_dir

# Initialize TensorFlow session.
# tf.InteractiveSession()
tf.compat.v1.InteractiveSession()

# Import official CelebA-HQ networks.
with open('karras2018iclr-lsun-bedroom-256x256.pkl', 'rb') as file:
    G, D, Gs = pickle.load(file)
    # G = Instantaneous snapshot of the generator, mainly useful for resuming a previous training run.
    # D = Instantaneous snapshot of the discriminator, mainly useful for resuming a previous training run.
    # Gs = Long-term average of the generator, yielding higher-quality results than the instantaneous snapshot.

# Generate latent vectors.
latents = np.random.RandomState(1000).randn(1000, *Gs.input_shapes[0][1:]) # 1000 random latents
latents = latents[[477, 56, 83, 887, 583, 391, 86, 340, 341, 415]] # hand-picked top-10

# Generate dummy labels (not used by the official networks).
labels = np.zeros([latents.shape[0]] + Gs.input_shapes[1][1:])

# Run the generator to produce a set of images.
images = Gs.run(latents, labels)

# Convert images to PIL-compatible format.
images = np.clip(np.rint((images + 1.0) / 2.0 * 255.0), 0.0, 255.0).astype(np.uint8) # [-1,1] => [0,255]
images = images.transpose(0, 2, 3, 1) # NCHW => NHWC

# # Save images as PNG.
# for idx in range(images.shape[0]):
#     PIL.Image.fromarray(images[idx], 'RGB').save('img%d.png' % idx)

# 使用 my_utils 中的函数创建存储图像的目录
save_dir = create_time_named_dir()

# Save images as PNG in the specific directory.
for idx in range(images.shape[0]):
    save_path = os.path.join(save_dir, f'img{idx}.png')
    PIL.Image.fromarray(images[idx], 'RGB').save(save_path)
