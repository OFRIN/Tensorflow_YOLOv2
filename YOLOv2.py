
import numpy as np
import tensorflow as tf
import resnet_v2.resnet_v2 as resnet_v2

from Define import *

initializer = tf.contrib.layers.xavier_initializer()

def conv_bn_relu(x, filters, kernel_size, strides, padding, is_training, scope, bn = True, activation = True, use_bias = True, upscaling = False):
    with tf.variable_scope(scope):
        if not upscaling:
            x = tf.layers.conv2d(inputs = x, filters = filters, kernel_size = kernel_size, strides = strides, padding = padding, kernel_initializer = initializer, use_bias = use_bias, name = 'conv2d')
        else:
            x = tf.layers.conv2d_transpose(inputs = x, filters = filters, kernel_size = kernel_size, strides = strides, padding = padding, kernel_initializer = initializer, use_bias = use_bias, name = 'upconv2d')
        
        if bn:
            x = tf.layers.batch_normalization(inputs = x, training = is_training, name = 'bn')

        if activation:
            x = tf.nn.relu(x, name = 'relu')
    return x

def Decode_Layer(pred_tensors, anchors):
    pred_cxcy = pred_tensors[..., :2]
    pred_wh = pred_tensors[..., 2:4]
    pred_conf = pred_tensors[..., 4]
    pred_classes = pred_tensors[..., 5:]

    pred_cxcy = tf.nn.sigmoid(pred_cxcy)
    pred_wh = tf.exp(pred_wh) * anchors
    pred_conf = tf.nn.sigmoid(pred_conf)[..., tf.newaxis]
    pred_classes = tf.nn.sigmoid(pred_classes)
    
    pred_tensors = tf.concat([pred_cxcy, pred_wh, pred_conf, pred_classes], axis = -1)
    return pred_tensors

def YOLOv2_ResNetv2_50(input_var, is_training, anchors, reuse = False):
    x = input_var - [103.939, 123.68, 116.779]
    with tf.contrib.slim.arg_scope(resnet_v2.resnet_arg_scope()):
        logits, end_points = resnet_v2.resnet_v2_50(x, is_training = is_training, reuse = reuse)
    
    for key in end_points.keys():
       print(key, end_points[key])
    
    with tf.variable_scope('YOLOv2', reuse = reuse):
        x = end_points['resnet_v2_50/block4']
        
        x = conv_bn_relu(x, B * (5 + CLASSES), [3, 3], 1, 'same', is_training, 'conv', bn = True, activation = False)
        pred_tensors = tf.reshape(x, (-1, S, S, B, 5 + CLASSES), name = 'pred_tensors')
        
    pred_tensors = Decode_Layer(pred_tensors, anchors)
    return pred_tensors

YOLOv2 = YOLOv2_ResNetv2_50

if __name__ == '__main__':
    from YOLOv2_Utils import *

    yolov2_utils = YOLOv2_Utils()
    input_var = tf.placeholder(tf.float32, [None, 416, 416, 3])
    
    pred_tensors = YOLOv2(input_var, False, yolov2_utils.anchors)
    print(pred_tensors)
