import tensorflow as tf
from tensorflow import keras

# TODO: write this into a configuration file
n_encoder_cells = 100  # Encoder time steps
n_decoder_cells = 28  # decoder time steps
n_length = n_encoder_cells + n_decoder_cells
n_neurons = 48  # neurons per cell
n_notes = 42  # number of different notes
learning_rate = 0.001  # learning rate


def _build_encoder_nn():
    encoder_inputs = keras.layers.Input(shape=[n_encoder_cells, n_notes, ], dtype=tf.float32)
    encoder_i = keras.layers.GRU(n_neurons,
                                 return_state=True,
                                 return_sequences=True)
    encoder_ii = keras.layers.GRU(n_neurons,
                                  return_state=True,
                                  return_sequences=True)
    encoder_iii = keras.layers.GRU(n_neurons, return_state=True)

    encoder_outputs_i, last_encoder_state_i = encoder_i(encoder_inputs)
    encoder_outputs_ii, last_encoder_state_ii = encoder_ii(encoder_outputs_i)
    _, last_encoder_state_iii = encoder_iii(encoder_outputs_ii)

    states = [last_encoder_state_i, last_encoder_state_ii, last_encoder_state_iii]

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
    decoder_iii = keras.layers.GRU(units=n_neurons,
                                   return_state=True,
                                   return_sequences=True)

    # connecting layers for training model
    decoder_outputs_i, _ = decoder_i(decoder_inputs, initial_state=states[0])
    decoder_outputs_ii, _ = decoder_ii(decoder_outputs_i, initial_state=states[1])
    decoder_outputs_iii, _ = decoder_ii(decoder_outputs_ii, initial_state=states[2])
    decoder_train_output = keras.layers.Dense(n_notes, activation='softmax')(decoder_outputs_iii)

    # redefining layers for inference model
    decoder_h_input_i = keras.layers.Input(shape=[n_neurons, ])
    decoder_h_input_ii = keras.layers.Input(shape=[n_neurons, ])
    decoder_h_input_iii = keras.layers.Input(shape=[n_neurons, ])
    decoder_states_input = [decoder_h_input_i, decoder_h_input_ii, decoder_h_input_iii]

    decoder_outputs_i, decoder_state_i = decoder_i(decoder_inputs, initial_state=decoder_h_input_i)
    decoder_outputs_ii, decoder_state_ii = decoder_ii(decoder_outputs_i, initial_state=decoder_h_input_ii)
    decoder_outputs_iii, decoder_state_iii = decoder_iii(decoder_outputs_ii, initial_state=decoder_h_input_iii)
    decoder_test_output = keras.layers.Dense(n_notes, activation='softmax')(decoder_outputs_iii)

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
        model = keras.Model(inputs=input_layer, outputs=states)
        return model

    def _decoder_test_model(self):
        d_inputs, _, d_states, test_outputs = self.decoder_prop
        return keras.Model(inputs=[d_inputs] + d_states, outputs=test_outputs)

    def _decoder_train_model(self):
        e_inputs, _ = self.encoder_prop
        d_inputs, train_outputs, _, _ = self.decoder_prop
        model = keras.Model(inputs=[e_inputs, d_inputs], outputs=train_outputs)
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def load_models(self, path: str):
        self.inf_enc = keras.models.load_model(path + '/inf_enc')
        self.inf_dec = keras.models.load_model(path + '/inf_dec')
        self.train_model = keras.models.load_model(path + '/train_model')

    def save_models(self, path='./trained_models'):
        self.inf_enc.save(path + '/inf_enc')
        self.inf_dec.save(path + '/inf_dec')
        self.train_model.save(path + '/train_model')
