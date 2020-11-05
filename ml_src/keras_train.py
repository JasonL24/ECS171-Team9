import numpy as np
import tensorflow as tf
import tensorflow_addons as tfa
from tensorflow import keras

if not tf.config.list_physical_devices('GPU'):
    print("No GPU was detected. LSTMs and CNNs can be very slow without a GPU.")
else:
    print("Congratulations, You are using GPU lol!")

# TODO: write this into a configuration file
n_encoder_cells = 48  # Encoder for 48 time steps
n_decoder_cells = 12  # decoder for 12 time steps
n_inputs = 2  # input pitch and velocity
n_neurons = 64  # 64 neurons per cell
n_notes = 12  # number of different notes
learning_rate = 0.001

# Embedding
# Music Theory
# Reinforcement Learning


encoder_inputs = keras.layers.Input(shape=[n_encoder_cells, n_inputs, ], dtype=tf.float32)
encoder_i = keras.layers.GRU(n_neurons,
                             return_state=True,
                             return_sequences=True,
                             input_shape=(n_encoder_cells, n_inputs))
encoder_ii = keras.layers.GRU(n_neurons, return_state=True)

# TODO: Add embedding layer later
# embeddings = keras.layers.Embedding(n, m)
# encoder_embeddings = embeddings(encoder_inputs)

<<<<<<< Updated upstream
encoder_outputs_i, last_encoder_state_i = encoder_i(encoder_inputs)
encoder_outputs_ii, last_encoder_state_ii = encoder_ii(encoder_outputs_i)

decoder_inputs = keras.layers.Input(shape=[n_decoder_cells, n_inputs, ], dtype=tf.float32)
decoder_i = keras.layers.GRU(units=n_neurons,
                             return_sequences=True,
                             input_shape=(n_decoder_cells, n_inputs))
decoder_ii = keras.layers.GRU(units=n_neurons,
                              return_sequences=True)

# connecting the layers
decoder_outputs_i = decoder_i(decoder_inputs, initial_state=last_encoder_state_i)
decoder_outputs_ii = decoder_ii(decoder_outputs_i, initial_state=last_encoder_state_ii)
output_layer = keras.layers.Dense(n_notes)(decoder_outputs_ii)

# skips the seq2seq basic decoder from the book
y_proba = tf.nn.softmax(output_layer)

model = keras.Model(inputs=[encoder_inputs, decoder_inputs], outputs=[y_proba])
model.compile(loss='categorical_cross_entropy', optimizer='adam')


def train(nn_input, nn_output):
    model.fit(x=nn_input,
              y=nn_output,
              epochs=100,
              batch_size=35)


if __name__ == '__main__':
    pass
    # train()
=======
    df = read_song('./temp.txt')
    df = encode_df(df)
    mini_batch = random_select_batch(df, 12, 7)
    df_x, df_y = split_data(mini_batch, 8, 4)
    y_shift = shift_y(df_y)

    train(models.train_model, df_x, y_shift, df_y)
>>>>>>> Stashed changes
