import tensorflow as tf
from models.utils import *
from models.custom_model import MusicNN

# TODO: features to do
# Embedding
# Music Theory
# Reinforcement Learning

if not tf.config.list_physical_devices('GPU'):
    print("No GPU was detected. LSTMs and CNNs can be very slow without a GPU.")
else:
    print("Congratulations, You are using GPU lol!")


def train(model, x, y_s, y):
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x=[x, y_s],
              y=y,
              epochs=1000,
              batch_size=1)


if __name__ == '__main__':
    models = MusicNN()

    df = read_song('./temp.txt')
    df = encode_df(df)
    batch = random_select_batch(df, 12, 10)
    df_x, df_y = split_data(batch, 8, 4)
    y_shift = shift_y(df_y)

    train(models.train_model, df_x, y_shift, df_y)
