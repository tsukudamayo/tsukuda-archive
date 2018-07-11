from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import tensorflow as tf

slim = tf.contrib.slim

def model_256x256(inputs,
                    num_classes=64,
                    is_training=True,
                    dropout_keep_prob=0.5,
                    spatial_squeeze=True,
                    scope='model_256x256',
                    global_pool=False):

  with tf.variable_scope(scope, 'model_256x256', [inputs]) as sc:
    end_points_collection = sc.original_name_scope + '_end_points'
    with slim.arg_scope([slim.conv2d, slim.fully_connected, slim.max_pool2d],
                        outputs_collections=[end_points_collection]):
      with slim.arg_scope([slim.conv2d, slim.fully_connected],
                          activation_fn=tf.nn.relu):
        net = slim.conv2d(inputs, 20, [5, 5], 1, padding='VALID', scope='conv1')
        print(sys.stdout.write('conv1 shape %s' % net.shape))
        net = slim.max_pool2d(net, [2, 2], padding='SAME', scope='pool1')
        print(sys.stdout.write('pool1 shape %s' % net.shape))
        net = slim.conv2d(net, 30, [5, 5], 1, padding='VALID', scope='conv2')
        print(sys.stdout.write('conv2 shape %s' % net.shape))
        net = slim.max_pool2d(net, [2, 2], padding='SAME', scope='pool2')
        print(sys.stdout.write('pool2 shape %s' % net.shape))
        net = slim.conv3d(net, 30, [5, 5], 1, padding='SAME', scope='conv3')
        print(sys.stdout.write('conv3 shape %s' % net.shape))
        net = slim.max_pool2d(net, [2, 2], padding='SAME', scope='pool3')
        print(sys.stdout.write('pool3 shape %s' % net.shape))

        # fully connected layers
        net = slim.flatten(net)
        net = tf.expand_dims(net, 1)
        net = tf.expand_dims(net, 2)
        net = slim.fully_connected(net, 803)
        net = slim.dropout(
            net, dropout_keep_prob, is_training=is_training, scope='dropout4'
        )
        print(sys.stdout.write('dropout4 shape %s' % net.shape))
        end_points = slim.utils.convert_collection_to_dict(
            end_points_collection
        )
        net = slim.conv2d(net, num_classes, [1, 1],
                          activation_fn=None,
                          normalizer_fn=None,
                          biases_initializer=tf.zeros_initializer(),
                          scope='fc5')
        print(sys.stdout.write('fc5 shape %s' % net.shape))
        if spatial_squeeze:
          net = tf.squeeze(net, [1, 2], name='fc5/squeezed')
          print(sys.stdout.write('fc5/squeezed %s' % net.shape))
        end_points[sc.name + '/fc5'] = net
    
        return net, end_points
model_256x256.default_image_size = 256

