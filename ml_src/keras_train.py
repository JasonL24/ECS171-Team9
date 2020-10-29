import numpy as np
import pandas as pd
import tensorflow as tf
from model_ops import *
# import tensorflow_addons as tfa
from tensorflow import keras
from tensorflow.keras.utils import plot_model
from models.custom_model import MusicNN

if not tf.config.list_physical_devices('GPU'):
    print("No GPU was detected. LSTMs and CNNs can be very slow without a GPU.")
else:
    print("Congratulations, You are using GPU lol!")


# Embedding
# Music Theory
# Reinforcement Learning

models = MusicNN()
# encoder_inputs = keras.layers.Input(shape=[n_encoder_cells, n_inputs, ], dtype=tf.float32)
# encoder_i = keras.layers.GRU(n_neurons,
#                              return_state=True,
#                              return_sequences=True,
#                              input_shape=(n_encoder_cells, n_inputs))
# encoder_ii = keras.layers.GRU(n_neurons, return_state=True)
#
# # TODO: Add embedding layer later
# # embeddings = keras.layers.Embedding(n, m)
# # encoder_embeddings = embeddings(encoder_inputs)
#+
# encoder_outputs_i, last_encoder_state_i = encoder_i(encoder_inputs)
# encoder_outputs_ii, last_encoder_state_ii = encoder_ii(encoder_outputs_i)
#
# decoder_inputs = keras.layers.Input(shape=[n_decoder_cells, n_inputs, ], dtype=tf.float32)
# decoder_i = keras.layers.GRU(units=n_neurons,
#                              return_sequences=True,
#                              input_shape=(n_decoder_cells, n_inputs))
# decoder_ii = keras.layers.GRU(units=n_neurons,
#                               return_sequences=True)
#
# # connecting the layers
# decoder_outputs_i = decoder_i(decoder_inputs, initial_state=last_encoder_state_i)
# decoder_outputs_ii = decoder_ii(decoder_outputs_i, initial_state=last_encoder_state_ii)
# output_layer = keras.layers.Dense(n_notes, activation='softmax')(decoder_outputs_ii)
#
# # skips the seq2seq basic decoder from the book
# y_proba = tf.nn.softmax(output_layer)

# model = keras.Model(inputs=[encoder_inputs, decoder_inputs], outputs=[y_proba])
# model.compile(loss='categorical_crossentropy', optimizer='adam')
# plot_model(model, to_file='./model.png', show_shapes=True)
#
#
# def train(nn_input, nn_output):
#     # fake_x = np.array()
#     # fake_y =
#     model.fit(x=[nn_input, nn_output],
#               y=nn_output,
#               epochs=100,
#               batch_size=1)


if __name__ == '__main__':
    df = get_dataframe()
    array = encode_df(df)
    dx, dy = split_data(12, 4, array)
    # train(dx, dy)
