"""Don't read this unless you REALLY want to understand the architecture.
This is a very low-level implementation of the RNN. For more modern use,
go to keras.train"""

import numpy as np
import tensorflow.compat.v1 as tf

# TODO: translate the code tensorflow2
tf.compat.v1.disable_eager_execution()

# TODO: Tune the steps and neuron to see the change in results
# Encoder for 48 steps
# Decoder for 12 steps. (Both highly composite numbers)
n_steps = 60
n_inputs = 2  # input pitch and velocity
n_neurons = 64  # 64 neurons per cell
n_outputs = 12  # output pitch and velocity

learning_rate = 0.001

X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
y = tf.placeholder(tf.int32, [None, n_outputs])

# TODO: try deep RNN and add more layers
rnn_LSTM_cell = tf.nn.rnn_cell.BasicLSTMCell(num_units=n_neurons)

# rnn_output holds the list of outputs for every cell
# rnn_states only holds the final state
rnn_outputs, rnn_states = tf.nn.dynamic_rnn(rnn_LSTM_cell, X, dtype=tf.float32)

# stacking the outputs
stacked_rnn_outputs = tf.reshape(rnn_outputs, [-1, n_neurons])

# create a logit layer for n_output number of cells
stacked_logits = tf.layers.dense(stacked_rnn_outputs, n_outputs, activation=tf.nn.tanh)

# unpacking the results
outputs = tf.reshape(stacked_logits, [-1, n_outputs, n_neurons])

# TODO: try different error estimation function
xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=outputs, name='error_est')
loss = tf.reduce_mean(xentropy)
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
training_op = optimizer.minimize(loss)
correct = tf.nn.in_top_k(outputs, y, 1)
accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))

init = tf.global_variables_initializer()
saver = tf.train.Saver()

n_epoch = 1500
batch_size = 20

# training session
with tf.Session() as sess:
    init.run()
    try:
        saver.restore(sess, './trained_models/music_synth_model')
    except FileNotFoundError:
        print('No previous model found')

    for epoch in range(n_epoch):
        x_batch, y_batch = 0, 0
        sess.run(training_op, feed_dict={X: x_batch, y: y_batch})
        if epoch % 10 == 0:
            acc_batch = accuracy.eval(feed_dict={X: x_batch, y: y_batch})
            # acc_test = accuracy.eval(feed_dict={X: X_test, y: y_test})
            print("Epoch:", epoch, "  Last batch accuracy: ", acc_batch, "Test accuracy:", 100)


print()
