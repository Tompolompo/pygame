import tensorflow as tf
device_name = tf.device.__name__
print(device_name)
with tf.device('/device:GPU:0'):
    device_name = tf.device.__name__
    print(device_name)