import tensorflow as tf

import_dir = 'saved_model/1/'
converter = tf.lite.TFLiteConverter.from_saved_model(import_dir)
tflite_model = converter.convert()
open('converted_model.tflite', 'wb').write(tflite_model)
