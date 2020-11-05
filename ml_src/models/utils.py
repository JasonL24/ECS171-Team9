import pandas as pd
import numpy as np
import random
from sklearn.preprocessing import OneHotEncoder

# increase the vocabs if we have new notations
_vocabs = ['A', 'B', 'C', 'D', 'E', 'F', 'G', '#', '0', 'A+']
_vocabs_length = len(_vocabs)
_vocabs_array = np.array(_vocabs).reshape((-1, 2))
_one_hot_enc = OneHotEncoder(handle_unknown='ignore')
_one_hot_enc.fit(_vocabs_array)


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
        raise ValueError
    if target_length > song_length:  # Target size is bigger than the length of the song
        raise ValueError

    # random sample
    samples = random.sample(range(song_length - target_length), batch_size)

    batch = np.zeros((batch_size, target_length, _vocabs_length))
    for i, j in zip(samples, range(batch_size)):
        line = df.loc[i: i + target_length - 1, :].to_numpy()
        batch[j, :, :] = line
    return batch


def read_song(file: str) -> pd.DataFrame:
    """ Parse the given txt file to pandas dataframe

    :param file: file path
    :return: a pandas dataframe of the song
    """
    df = pd.DataFrame([[0, 0]], columns=[0, 1])
    with open(file) as file:
        for i, line in zip(range(28), file):
            line = line.split()
            line.pop(0)
            series = pd.Series(line, index=[0, 1])
            df.loc[i] = series
    return df


def encode_df(df: pd.DataFrame()) -> pd.DataFrame:
    encoded = _one_hot_enc.transform(df.to_numpy()).toarray()
    return pd.DataFrame(encoded)


def split_data(batch: np.array, x_size: int, y_size: int):
    y = batch.shape[1]
    if x_size + y_size > batch.shape[1]:
        raise ValueError
    x = batch[:, 0: x_size, :]
    y = batch[:, x_size: x_size + y_size, :]
    return x, y


def shift_y(y: np.array):
    batch_size = y.shape[0]
    zeros = np.zeros([batch_size, 1, _vocabs_length])
    y_shift = np.concatenate([zeros, y], axis=1)
    return y_shift[:, :-1, :]


def organize_data(x, y):
    y_shift = shift_y(y)
    x = np.concatenate([x, y_shift])
    return x, y


if __name__ == '__main__':
    # Testing
    song_df = read_song('./temp.txt')
    song_df = encode_df(song_df)
    mini_batch = random_select_batch(song_df, 6, 7)
    dx, dy = split_data(mini_batch, 4, 2)
    s_dy = shift_y(dy)
    print()
