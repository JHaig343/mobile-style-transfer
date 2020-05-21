# Arbitrary Stylization - A faster version of the neural style transfer algorithm
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import PIL.Image
import matplotlib.pyplot as plt


def tensor_to_image(tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return PIL.Image.fromarray(tensor)


# load image and limit dimension to 512 pixels
def load_img(path_to_img):
    max_dim = 719
    img = tf.io.read_file(path_to_img)
    # three color channels - R G B
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img


# Function version of code above, for calling from Flask server
def draw_image_stylized(content_img, style_img, savename):
    content_image = load_img(content_img)
    style_image = load_img(style_img)
    # The TF Hub model we want to use - arbitrary neural style transfer
    hub_handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
    hub_module = hub.load(hub_handle)
    outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
    stylized_image = outputs[0]
    converted_img = tensor_to_image((stylized_image))
    converted_img.save(savename, "PNG")