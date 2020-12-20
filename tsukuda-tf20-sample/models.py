import tensorflow as tf


def create_model():
    METRICS = [
        tf.keras.metrics.TruePositives(name='tp'),
        tf.keras.metrics.FalsePositives(name='fp'),
        tf.keras.metrics.TrueNegatives(name='tn'),
        tf.keras.metrics.FalseNegatives(name='fn'),
        tf.keras.metrics.Accuracy(name='accuracy'),
        tf.keras.metrics.Precision(name='precision'),
        tf.keras.metrics.Recall(name='recall'),
        tf.keras.metrics.AUC(name='roc'),
        tf.keras.metrics.AUC(name='pr', curve='PR')
    ]
    
    model = tf.keras.applications.MobileNet(
        input_shape=(224, 224, 3),
        alpha=0.5,
        weights=None,
        classes=20,
    )

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=METRICS
    )

    return model



    # # TODO using model map
    # ------------ #
    # tutorial net #
    # ------------ #
    # model = Sequential(
    #     [
    #      Conv2D(16, 3, padding='same', activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    #      MaxPooling2D(),
    #      Conv2D(32, 3, padding='same', activation='relu'),
    #      MaxPooling2D(),
    #      Conv2D(64, 3, padding='same', activation='relu'),
    #      MaxPooling2D(),
    #      Flatten(),
    #      Dense(512, activation='relu'),
    #      Dense(20, activation='softmax')
    #      ]
    # )
