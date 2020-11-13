import os
from models.utils import *
from models.custom_model import *

dataset_dir = '../data_mining/parsed_data/'
big_epoch = 5

# TODO: features to do
# Music Theory
# Reinforcement Learning

if not tf.config.list_physical_devices('GPU'):
    print("No GPU was detected. LSTMs and CNNs can be very slow without a GPU.")
else:
    print("Congratulations, You are using GPU lol!")


def train(model, x, y_s, y):
    model.fit(x=[x, y_s],
              y=y,
              epochs=50,
              batch_size=5)


if __name__ == '__main__':
    models = MusicNN()
    for _ in range(big_epoch):
        for filename in os.listdir(dataset_dir):
            song_df = read_song(dataset_dir + filename, 'Piano left')
            song_df = encode_df(song_df)
            mini_batch = random_select_batch(song_df, n_length, 500)
            dx, dy = split_data(mini_batch, n_encoder_cells, n_decoder_cells)
            s_dy = shift_y(dy)

            try:
                train(models.train_model, dx, dy, s_dy)
            except KeyboardInterrupt:
                models.save_models()
    models.save_models()
    
