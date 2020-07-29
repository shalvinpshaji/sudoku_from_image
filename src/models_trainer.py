import tensorflow as tf


def changer(x, y):
    for one in range(len(y)):
        if y[one] == 0:
            x[one] = x[one] * 0
    return x


callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)
mnist = tf.keras.datasets.mnist
(xtrain, ytrain), (xtest, ytest) = mnist.load_data()
xtrain, xtest = xtrain / 255.0, xtest / 255.0
xtrain = xtrain.reshape(60000, 28, 28, 1)
xtrain = changer(xtrain, ytrain)
xtest = xtest.reshape(10000, 28, 28, 1)
xtest = changer(xtest, ytest)
ytrain = tf.keras.utils.to_categorical(ytrain)
ytest = tf.keras.utils.to_categorical(ytest)
model = tf.keras.Sequential()
model.add(tf.keras.layers.Conv2D(input_shape=(28, 28, 1), filters=32, kernel_size=(3, 3), activation="relu"))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(512, activation="relu"))
model.add(tf.keras.layers.Dense(10, activation="softmax"))
model.summary()
model.compile(optimizer='adam', loss="categorical_crossentropy", metrics=['accuracy'])
model.fit(xtrain, ytrain, epochs=5, callbacks=[callback])
model.evaluate(xtest, ytest)
model.save("model_cus.h5")
