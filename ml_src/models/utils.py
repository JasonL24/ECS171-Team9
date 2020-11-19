import random
import os
import pandas as pd
import numpy as np
from models.define import *
from sklearn.preprocessing import OneHotEncoder

_pitch_vocabs = list(range(60, 85)) + [0]
_pitch_vocabs_length = len(_pitch_vocabs)

_vel_vocabs = list(range(40, 75)) + [0]
_vel_vocabs_length = len(_vel_vocabs)
_combined_length = _pitch_vocabs_length + _vel_vocabs_length

_pitch_enc = OneHotEncoder(handle_unknown='ignore')
_pitch_enc.fit(np.array(_pitch_vocabs).reshape([-1, 1]))

_vel_enc = OneHotEncoder(handle_unknown='ignore')
_vel_enc.fit(np.array(_vel_vocabs).reshape([-1, 1]))


def random_select_batch(df: pd.DataFrame, target_length: int, batch_size: int = 1) -> np.array:
    """ randomly select batch_size number of samples of each x_size + y_size. The input should
    be one song only. The maximum number of batch should be len(song) - 2

    :param df: target song to parse
    :param target_length: size of input + output
    :param batch_size:
    :return: a list of randomly selected batch size input un-shifted
    """
    song_length = len(df)

    if batch_size > song_length - target_length + 1:  # So we don't select overlapping samples
        print('Batch size too big', str(song_length))
        raise ValueError
    if target_length > song_length:  # Target size is bigger than the length of the song
        print('Target length is longer than song', str(song_length))
        raise ValueError

    # random sample
    samples = random.sample(range(song_length - target_length), batch_size)

    batch = np.zeros((batch_size, target_length, _combined_length))
    for i, j in zip(samples, range(batch_size)):
        line = df.loc[i: i + target_length - 1, :].to_numpy()
        batch[j, :, :] = line
    return batch


def read_song(file: str, part: str) -> pd.DataFrame:
    """ Parse the given txt file to pandas dataframe

    :param file: file path
    :param part: the targeted part of the song
    :return: a pandas dataframe of the song
    """
    df = pd.DataFrame([[0, 0]], columns=[0, 1])
    with open(file) as file:
        read = False
        for i, line in enumerate(file):
            if line[0] == "\"":
                continue  # song name
            if line[0] == "#":
                line = line.split()
                if line[1:] == part.split():  # check if it's target part
                    read = not read
                    continue
                if read:  # end reading
                    break
            if read:
                line = line.split()
                line = [int(x) for x in line[1:]]
                series = pd.Series(line, index=[0, 1])
                df.loc[i] = series
    return df


def encode_df(df: pd.DataFrame()) -> pd.DataFrame:
    pitch_enc = _pitch_enc.transform(df[0].to_numpy().reshape((-1, 1))).toarray()
    vel_enc = _vel_enc.transform(df[1].to_numpy().reshape(-1, 1)).toarray()
    combined = np.concatenate([pitch_enc, vel_enc], axis=1)
    return pd.DataFrame(combined)


def split_data(batch: np.array, x_size: int, y_size: int):
    if x_size + y_size > batch.shape[1]:
        raise ValueError
    x = batch[:, 0: x_size, :]
    y = batch[:, x_size: x_size + y_size, :]
    return x, y


def shift_y(y: np.array):
    batch_size = y.shape[0]
    zeros = np.zeros([batch_size, 1, _combined_length])
    y_shift = np.concatenate([zeros, y], axis=1)
    return y_shift[:, :-1, :]


def organize_data(x, y):
    y_shift = shift_y(y)
    x = np.concatenate([x, y_shift])
    return x, y


def batch_randomize(batches: list) -> np.array:
    batches = np.concatenate(batches, axis=0)
    np.random.shuffle(batches)
    return batches


def generate_data(dataset_dir, part, n):
    batches = list()
    for filename in os.listdir(dataset_dir):
        print(filename)
        song_df = read_song(dataset_dir + filename, part)
        song_df = encode_df(song_df)
        try:
            batches.append(random_select_batch(song_df, n_length, 100))
        except ValueError:
            continue

    batches = batch_randomize(batches)
    dx, dy = split_data(batches, n_encoder_cells, n_decoder_cells)
    s_dy = shift_y(dy)
    np.save('./dataset/encoder_data_' + n + '.npy', dx)
    np.save('./dataset/decoder_data_' + n + '.npy', dy)
    np.save('./dataset/shifted_decoder_data_' + n + '.npy', s_dy)


def load_train_data(n):
    dx = np.load('./dataset/encoder_data_' + n + '.npy')
    dy = np.load('./dataset/decoder_data_' + n + '.npy')
    s_dy = np.load('./dataset/shifted_decoder_data_' + n + '.npy')
    return dx, s_dy, dy


def generate_sequences():
    rand_pitch = list()
    rand_vel = list()
    for i in range(n_length):
        rand_pitch.append(random.choice(_pitch_vocabs))
        rand_vel.append(random.choice(_vel_vocabs))

    enc_seq = np.array([rand_pitch[0:n_encoder_cells], rand_vel[0:n_encoder_cells]])
    dec_seq = np.array([rand_pitch[n_encoder_cells:], rand_vel[n_encoder_cells:]])
    enc_seq = encode_df(pd.DataFrame(data=enc_seq.reshape((-1, 2)), columns=[0, 1])).to_numpy()
    dec_seq = encode_df(pd.DataFrame(data=dec_seq.reshape((-1, 2)), columns=[0, 1])).to_numpy()
    enc_seq = enc_seq.reshape([1, n_encoder_cells, n_notes])
    dec_seq = dec_seq.reshape([1, n_decoder_cells, n_notes])
    return enc_seq, dec_seq


def song_threshold(song: np.array):
    pitch = song[:, 0:_pitch_vocabs_length]
    velocity = song[:, _pitch_vocabs_length:]
    pitch = np.argmax(pitch, axis=1)
    velocity = np.argmax(velocity, axis=1)
    return pitch, velocity

#
# if __name__ == '__main__':
#     x, y = generate_sequences()
#     print()
