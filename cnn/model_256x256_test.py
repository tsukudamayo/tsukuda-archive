"""Tests for 256x256"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from nets import model_256x256

slim = tf.contrib.slim


class Model256x256Test(tf.test.TestCase):

    def testBuild(self):
        batch_size = 5
        height, width = 256, 128
        num_classes = 64
        with self.test_session():
            inputs = tf.random_uniform((batch_size, height, width, 3))
            logits, _ = model_256x256.model_256x256(inputs, num_classes)
            self.assertEquals(logits.op.name, '256x256/fc5/squeezed')
            self.assertListEqual(logits.get_shape().as_list(),
                                 [batch_size, num_classes])
            
