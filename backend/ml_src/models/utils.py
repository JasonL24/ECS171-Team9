import os
import random
import pickle
import pandas as pd
import numpy as np
from .define import *
from sklearn.cluster import KMeans
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

_lof_filter = LocalOutlierFactor(n_neighbors=n_notes)
_kMeans = KMeans(n_clusters=n_notes, random_state=0)

_k_vocabs = list(range(0, n_notes))
_kMeans_enc = OneHotEncoder(handle_unknown='ignore')
_kMeans_enc.fit(np.array(_k_vocabs).reshape([-1, 1]))


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

    batch = np.zeros((batch_size, target_length, 2))
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


def encode_df(array: np.array) -> np.array:
    return np.array(_kMeans_enc.transform(array).toarray())


def split_data(batch: np.array, x_size: int, y_size: int):
    if x_size + y_size > batch.shape[1]:
        raise ValueError
    x = batch[:, 0: x_size, :]
    y = batch[:, x_size: x_size + y_size, :]
    return x, y


def shift_y(y: np.array):
    batch_size = y.shape[0]
    zeros = np.zeros([batch_size, 1, n_notes])
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


def clustering_notes(notes_dict: list, batches: np.array, n) -> np.array:
    notes_dict = np.concatenate(notes_dict)
    # batches = np.concatenate(batches)

    outliers = np.array(_lof_filter.fit_predict(notes_dict))
    outliers_index = np.where(outliers == -1)
    notes_dict = np.delete(notes_dict, outliers_index[0], axis=0)
    _kMeans.fit(notes_dict)

    pickle.dump(_kMeans, open("./dataset/kmeans_" + n + ".sklearn", 'wb'))
    print('Outliers: ', len(outliers_index[0]))

    tmp_batches = list()
    for batch in batches:
        tmp_batch = list()
        for step in batch:
            k_batch = _kMeans.predict(step.reshape(1, 2))
            tmp_batch.append(k_batch)
        encoded_k = encode_df(np.array(tmp_batch).reshape((-1, 1)))
        tmp_batches.append(encoded_k)
    return np.array(tmp_batches)


def generate_data(dataset_dir, part, n):
    batches = list()
    notes_dict = list()
    for filename in os.listdir(dataset_dir):
        print(filename)
        song_df = read_song(dataset_dir + filename, part)
        try:
            notes_dict.append(song_df)
            batches.append(random_select_batch(song_df, n_length, 100))
        except ValueError:
            continue

    batches = batch_randomize(batches)
    batches = clustering_notes(notes_dict, batches, n)
    dx, dy = split_data(batches, n_encoder_cells, n_decoder_cells)
    s_dy = shift_y(dy)

    np.save('./dataset/encoder_data_' + n + '.npy', dx)
    np.save('./dataset/decoder_data_' + n + '.npy', dy)
    np.save('./dataset/shifted_decoder_data_' + n + '.npy', s_dy)


def load_train_data(n, ratio=0.2):
    dx = np.load('./dataset/encoder_data_' + n + '.npy')
    dy = np.load('./dataset/decoder_data_' + n + '.npy')
    s_dy = np.load('./dataset/shifted_decoder_data_' + n + '.npy')

    train_dx, test_dx, train_dy, test_dy, train_sdy, test_sdy = \
        train_test_split(dx, dy, s_dy, test_size=ratio)
    return [train_dx, train_sdy, train_dy], [test_dx, test_sdy, test_dy]


def better_seq(n):
    data, _ = load_train_data(n, 0.99)
    dx = data[0]
    sdy = data[1]
    return dx[0:1, :, :], sdy[0:1, :, :]


def generate_sequences():
    rand_seq = list()
    for i in range(n_length):
        if i == n_encoder_cells:
            rand_seq.append(0)
            continue
        rand_seq.append(random.choice(_k_vocabs))

    enc_seq = np.array(rand_seq[0:n_encoder_cells]).reshape((-1, 1))
    dec_seq = np.array(rand_seq[n_encoder_cells:]).reshape((-1, 1))
    enc_seq = encode_df(enc_seq)
    dec_seq = encode_df(dec_seq)
    enc_seq = enc_seq.reshape([1, n_encoder_cells, n_notes])
    dec_seq = dec_seq.reshape([1, n_decoder_cells, n_notes])
    # return np.zeros((1, n_encoder_cells, n_notes)), np.zeros((1, n_decoder_cells, n_notes))
    return enc_seq, dec_seq


def song_threshold(song: np.array):
    song = np.argmax(song, axis=1)
    return song


def random_length():
    x = random.choice(list(range(60, 120)))
    return int(x / 0.07)


def decode_song(song, n):
    k_mean_model = pickle.load(open("./ml_src/dataset/kmeans_" + n + ".sklearn", 'rb'))
    centers = k_mean_model.cluster_centers_
    # print(centers)
    dec_pitch = list()
    dec_vel = list()
    for note in song:
        dec_pitch.append(int(centers[note, 0]))
        dec_vel.append(int(centers[note, 1]))
    return dec_pitch, dec_vel


if __name__ == '__main__':
    generate_data('../data_mining/database/classical/', 'Piano right', '4')
    print()
