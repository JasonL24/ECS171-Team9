import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder


def get_dataframe():
    _df = pd.DataFrame([[0, 0]], columns=[0, 1])
    with open('temp.txt') as file:
        for i, line in zip(range(28), file):
            line = line.split()
            line.pop(0)
            series = pd.Series(line, index=[0, 1])
            _df.loc[i] = series
    return _df


def encode_df(df):
    one_hot = OneHotEncoder()
    encoded = one_hot.fit_transform(df.to_numpy()).toarray()
    return encoded


def split_data(x_size, y_size, df):
    x = df[0: x_size, :]
    y = df[x_size: x_size + y_size, :]
    return x, y


def shift_y():
    pass


def match_dim(x: np.ndarray, y: np.ndarray):
    shape_x = x.shape
    shape_y = y.shape
    diff = shape_x[0] - shape_y[0]
    zeros = np.zeros([diff, shape_y[1]])
    temp = np.concatenate([zeros, y])
    return x, temp


if __name__ == '__main__':
    frame = get_dataframe()
    frame = encode_df(frame)
    dx, dy = split_data(12, 4, frame)
    dx, dy = match_dim(dx, dy)
    print()