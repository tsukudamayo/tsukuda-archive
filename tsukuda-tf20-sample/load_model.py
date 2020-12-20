import tensorflow as tf

model_dir = './saved_model/1'


imported = tf.saved_model.load(model_dir)
print('imported')
print(imported)
print(list(imported.signatures.keys()))
infer = imported.signatures['serving_default']
print(infer.structured_outputs)



