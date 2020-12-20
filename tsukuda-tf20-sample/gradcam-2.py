import numpy as np
import cv2

import tensorflow as tf
from tensorflow.python.framework import ops
import tensorflow.keras.backend as K
from tensorflow.keras.preprocessing import image


_TEST_DATA = './data/test_data/cp_rand_front_1.jpg'
_CHECKPOINT_DIR = './training_1'


def process_image(img_path):
    img = image.load_img(img_path, target_size=(224,224))
    image.save_img('load.jpg', img)
    img_array = image.img_to_array(img)
    extended_img_array = np.expand_dims(img_array, axis=0)
    pimg = tf.keras.applications.mobilenet.preprocess_input(
        extended_img_array
    )

    return pimg


def create_model():
    model = tf.keras.applications.MobileNet(
        input_shape=(224, 224, 3),
        alpha=0.5,
        weights=None,
        classes=20,
    )
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy'],
    )

    return model


def target_category_loss(x, category_index, num_of_class):
    return tf.multiply(x, tf.one_hot([category_index], num_of_class))


def target_category_loss_output_shape(input_shape):
    return input_shape


def normalize(x):
    return x / (K.sqrt(K.mean(K.square(x))) + 1e-5)


def grad_cam(input_model, image, category_index, layer_name, num_of_class):
    target_layer = lambda x: target_category_loss(x, category_index, num_of_class)
    print('target_layer : ', target_layer)
    x = input_model.layers[-1].output
    print('x')
    print(x)
    x = tf.keras.layers.Lambda(target_layer, output_shape=target_category_loss_output_shape)(x)
    print('x')
    print(x)
    model = tf.keras.models.Model(input_model.layers[0].input, x)
    print('model')
    print(model)

    loss = K.sum(model.layers[-1].output)
    print(model.layers[-1].output)
    print('layer_name : ', layer_name)
    # for l in model.layers:
    #     print('name : ', l.name)
    #     print('layer_name : ', layer_name)
    #     print(l.name == layer_name)
    conv_output = [l for l in model.layers if l.name == layer_name][0].output
    print('conv_output : ', conv_output.shape)
    print('loss : ', loss.shape)

    grads = normalize(tf.keras.backend.gradients(loss, conv_output)[0])
    gradient_function = K.function([model.layers[0].input], [conv_output, grads])

    output, grads_val = gradient_function([image])
    output, grads_val = output[0, :], grads_val[0, :, :, :]

    weights = np.mean(grads_val, axis=(0, 1))
    cam = np.ones(output.shape[0:2], dtype=np.float32)

    for i, w in enumerate(weights):
        cam += w * output[:, :, i]

    cam = cv2.resize(cam, (224, 224))
    cv2.imwrite('resize.jpg', cam)
    cam = np.maximum(cam, 0)
    heatmap = cam / np.max(cam)

    cv2.imwrite('image1.jpg', image)
    image = image[0, :]
    image -= np.min(image)
    image = np.minimum(image, 255)

    cam = cv2.applyColorMap(np.uint8(255*heatmap), cv2.COLORMAP_JET)
    cam = np.float32(cam) + np.float32(image)
    cam = 255 * cam / np.max(cam)

    return np.uint8(cam), heatmap


def register_gradient():
    if "GuidedBackProp" not in ops._gradient_registry._registry:
        @ops.RegisterGradient("GuidedBackProp")
        def _GuidedBackProp(op, grad):
            dtype = op.inputs[0].dtype
            return grad * tf.cast(grad > 0., dtype) * tf.cast(op.inputs[0] > 0., dtype)

def compile_saliency_function(model, graph, activation_layer='conv_pw_13_relu'):
    with graph.as_default():
        input_img = model.input
        layer_dict = dict([(layer.name, layer) for layer in model.layers[1:]])
        layer_output = layer_dict[activation_layer].output
        max_output = K.max(layer_output, axis=3)
        saliency = K.gradients(K.sum(max_output), input_img)[0]
        return K.function([input_img, K.learning_phase()], [saliency])
def modify_backprop(model, name, graph):
    with graph.as_default():
        with graph.gradient_override_map({'Relu': name}):
            layer_dict = [layer for layer in model.layers[1:]
                          if hasattr(layer, 'activation')]
            for layer in layer_dict:
                if layer.activation == tf.keras.activations.relu:
                    layer.activation = tf.nn.relu
            new_model = tf.keras.applications.MobileNet(weights='imagenet')
        return new_model, graph


def deprocess_image(x):

    if np.ndim(x) > 3:
        x = np.squeeze(x)
    x -= x.mean()
    x /= (x.std() + 1e-5)
    x *= 0.1
    x += 0.5
    x = np.clip(x, 0, 1)
    x *= 255
    if K.image_data_format() == 'channels_first':
        x = x.transpose((1, 2, 0))
    x = np.clip(x, 0, 255).astype('uint8')
    return x


def main():
    g = tf.Graph()
    with g.as_default():

        model = create_model()
        model.summary()
        latest = tf.train.latest_checkpoint(_CHECKPOINT_DIR)
        model.load_weights(latest)
        
        params = model.get_layer(name='conv_pw_13_relu')
        print('params')
        print(type(params))
        print(params.dtype)

        pimg = process_image(_TEST_DATA)
        print('process_image : ', pimg.shape)
        prediction = model.predict(pimg)
        print(prediction)
        top = np.argmax(prediction)
        print('top')
        print(top)
        
        cam, heatmap = grad_cam(model, pimg, top, 'conv_pw_13_relu', 20)
        cv2.imwrite('gradcam.jpg', cam)
        cv2.imwrite('heatmap.jpg', heatmap)

        register_gradient()
        guided_model, graph = modify_backprop(model, 'GuidedBackProp', g)
        saliency_fn = compile_saliency_function(guided_model, g)
        saliency = saliency_fn([pimg, 0])
        gradcam = saliency[0] * heatmap[..., np.newaxis]
        cv2.imwrite('guided_backprop.jpg', deprocess_image(saliency[0]))
        cv2.imwrite('guided_gradcam.jpg', deprocess_image(gradcam))


if __name__ == '__main__':
    main()
