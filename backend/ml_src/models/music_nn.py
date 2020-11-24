import tensorflow as tf
from tensorflow import keras
from .define import *
import numpy as np

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
    decoder_states_output = [decoder_state_i, decoder_state_ii, decoder_state_iii]

    return [decoder_inputs, decoder_train_output, decoder_states_input, decoder_test_output, decoder_states_output]


class MusicNN:
    def __init__(self):
        self.encoder_prop = _build_encoder_nn()
        self.decoder_prop = _build_decoder_nn(self.encoder_prop[1])
        self.inf_enc = self._encoder_model()
        self.inf_dec = self._decoder_test_model()
        self.train_model = self._decoder_train_model()
        self.path = './ml_src/trained_models'

    def _encoder_model(self):
        input_layer, states = self.encoder_prop
        model = keras.Model(inputs=input_layer, outputs=states)
        return model

    def _decoder_test_model(self):
        d_inputs, _, d_states, test_outputs, test_states = self.decoder_prop
        return keras.Model(inputs=[d_inputs] + d_states, outputs=[test_outputs] + test_states)

    def _decoder_train_model(self):
        e_inputs, _ = self.encoder_prop
        d_inputs, train_outputs, _, _, _ = self.decoder_prop
        model = keras.Model(inputs=[e_inputs, d_inputs], outputs=train_outputs)
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def load_weights(self, path):
        self.inf_enc.load_weights(path + '/inf_enc.h5')
        self.inf_dec.load_weights(path + '/inf_dec.h5')
        self.train_model.load_weights(path + '/train_model.h5')

    def save_models(self):
        self.inf_enc.save(self.path + '/big_set/inf_enc.h5')
        self.inf_dec.save(self.path + '/big_set/inf_dec.h5')
        self.train_model.save(self.path + '/big_set/train_model.h5')

    def set_path(self, path):
        self.path = path

    def generate_songs(self, enc_src, dec_src, length):
        pre_seq = enc_src
        target_seq = dec_src
        song = list()
        states = self.inf_enc.predict(pre_seq)

        for t in range(length):
            y_pred, state_1, state_2, state_3 = self.inf_dec.predict(x=[target_seq] + states)
            song.append(y_pred[0, 0, :])
            states = [state_1, state_2, state_3]

            y_pred = y_pred[0, :, :]
            b = np.zeros_like(y_pred)
            b[np.arange(n_decoder_cells), np.argmax(y_pred, axis=1)] = 1
            y_pred = b
            target_seq = y_pred.reshape((1, n_decoder_cells, n_notes))
            if t % 10 == 0:
                print(t)
        return song
