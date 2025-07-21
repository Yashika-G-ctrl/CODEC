import tensorflow as tf
from tensorflow.keras import layers, models
(x, y), (vx, vy) = tf.keras.datasets.cifar10.load_data()
x, vx = x/255.0, vx/255.0
m = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(32,32,3)),
    layers.MaxPooling2D(2,2),
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])
m.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
m.fit(x, y, epochs=10, validation_data=(vx, vy))
m.save('model/model.h5')
print('model saved')
