import tensorflow as tf
from tensorflow import keras

# TODO: write this into a configuration file
n_encoder_cells = 8  # Encoder time steps
n_decoder_cells = 4  # decoder time steps
n_neurons = 512  # neurons per cell
n_notes = 10  # number of different notes
learning_rate = 0.001  # learning rate

if not tf.config.list_physical_devices('GPU'):
    print("No GPU was detected. LSTMs and CNNs can be very slow without a GPU.")
else:
    print("Congratulations, You are using GPU lol!")


def _build_encoder_nn():
    encoder_inputs = keras.layers.Input(shape=[n_encoder_cells, n_notes, ], dtype=tf.float32)
    encoder_i = keras.layers.GRU(n_neurons,
                                 return_state=True,
                                 return_sequences=True)
    encoder_ii = keras.layers.GRU(n_neurons, return_state=True)

    encoder_outputs_i, last_encoder_state_i = encoder_i(encoder_inputs)

    _, last_encoder_state_ii = encoder_ii(encoder_outputs_i)

    states = [last_encoder_state_i, last_encoder_state_ii]

    return [encoder_inputs, states]


def _build_encoder_nn_multiple_layer(num_of_layers):
    encoder_inputs = keras.layers.Input(shape=[n_encoder_cells, n_notes, ], dtype=tf.float32)

    encoder_layer = []
    encoder_outputs = []
    last_encoder_state = []

    for i in range(num_of_layers):
        current_layer = keras.layers.GRU(n_neurons,
                                         return_state=True,
                                         return_sequences=True)
        encoder_layer.append(current_layer)

        if i == 0:
            temp1, temp2 = current_layer(encoder_inputs)
        else:
            temp1, temp2 = current_layer(encoder_outputs[-1])

        encoder_outputs.append(temp1)
        last_encoder_state.append(temp2)
    states = last_encoder_state

    return [encoder_inputs, states]


def _build_decoder_nn(states):
    decoder_inputs = keras.layers.Input(shape=[n_decoder_cells, n_notes, ], dtype=tf.float32)

    # create decoder layers
    decoder_i = keras.layers.GRU(units=n_neurons,
                                 return_state=True,
                                 return_sequences=True)
    decoder_ii = keras.layers.GRU(units=n_neurons,
                                  return_state=True,
                                  return_sequences=True)

    # connecting layers for training model
    decoder_outputs_i, _ = decoder_i(decoder_inputs, initial_state=states[0])
    decoder_outputs_ii, _ = decoder_ii(decoder_outputs_i, initial_state=states[1])
    decoder_train_output = keras.layers.Dense(n_notes, activation='softmax')(decoder_outputs_ii)

    # redefining layers for inference model
    decoder_h_input_i = keras.layers.Input(shape=[n_neurons, ])
    decoder_h_input_ii = keras.layers.Input(shape=[n_neurons, ])
    decoder_states_input = [decoder_h_input_i, decoder_h_input_ii]

    decoder_outputs_i, decoder_state_i = decoder_i(decoder_inputs, initial_state=decoder_h_input_i)
    decoder_outputs_ii, decoder_state_ii = decoder_ii(decoder_outputs_i, initial_state=decoder_h_input_ii)
    decoder_test_output = keras.layers.Dense(n_notes, activation='softmax')(decoder_outputs_ii)

    return [decoder_inputs, decoder_train_output, decoder_states_input, decoder_test_output]


def _build_decoder_nn_multiple_layer(num_of_layers, states):
    decoder_inputs = keras.layers.Input(shape=[n_decoder_cells, n_notes, ], dtype=tf.float32)

    # create decoder layers
    decoder_layer = []
    for i in range(num_of_layers):
        decoder_layer.append(keras.layers.GRU(units=n_neurons,
                                              return_state=True,
                                              return_sequences=True))
    decoder_outputs = []
    for i in range(num_of_layers):
        if i == 0:
            temp1, _ = decoder_layer[i](decoder_inputs, initial_state=states[i])
        else:
            temp1, _ = decoder_layer[i](decoder_outputs[i - 1], initial_state=states[i])
        decoder_outputs.append(temp1)

    decoder_train_output = keras.layers.Dense(n_notes, activation='softmax')(decoder_outputs[-1])

    # redefining layers for inference model
    decoder_h_input = []
    for i in range(num_of_layers):
        decoder_h_input.append(keras.layers.Input(shape=[n_neurons, ]))
    decoder_states_input = decoder_h_input
    decoder_outputs = []
    decoder_state = []
    for i in range(num_of_layers):
        if i == 0:
            temp1, temp2 = decoder_layer[i](decoder_inputs, initial_state=decoder_h_input[i])
        else:
            temp1, temp2 = decoder_layer[i](temp1, initial_state=decoder_h_input[i])
    decoder_test_output = keras.layers.Dense(n_notes, activation='softmax')(temp1)

    return [decoder_inputs, decoder_train_output, decoder_states_input, decoder_test_output]


class MusicNN:
    # TODO: Add embedding layer later
    # embeddings = keras.layers.Embedding(n, m)
    # encoder_embeddings = embeddings(encoder_inputs)
    def __init__(self):
        self.encoder_prop = _build_encoder_nn()
        self.decoder_prop = _build_decoder_nn(self.encoder_prop[1])
        self.inf_enc = self._encoder_model()
        self.inf_dec = self._decoder_test_model()
        self.train_model = self._decoder_train_model()

    def _encoder_model(self):
        input_layer, states = self.encoder_prop
        return keras.Model(inputs=input_layer, outputs=states)

    def _decoder_test_model(self):
        d_inputs, _, d_states, test_outputs = self.decoder_prop
        return keras.Model(inputs=[d_inputs] + d_states, outputs=test_outputs)

    def _decoder_train_model(self):
        e_inputs, _ = self.encoder_prop
        d_inputs, train_outputs, _, _ = self.decoder_prop
        return keras.Model(inputs=[e_inputs, d_inputs], outputs=train_outputs)
