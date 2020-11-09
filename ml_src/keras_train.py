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
    data = get_words()
    vocab_size=1000
    encoded=[]
    y=[]  # ignore just for testing
    max_len = 25
    # encode text to ints
    for d in data:
        encoded.append(tf.keras.preprocessing.text.one_hot(d,vocab_size))
        y.append(0) # ignore just for testing

    # pad the int arrays by max_len
    padded=tf.keras.preprocessing.sequence.pad_sequences(encoded,maxlen=max_len,padding='post',value=0.0)
    padded = np.array(padded)
    y = np.array(y)
    #models._embed_model(padded, y, max_len)
    models.train_model.summary()
    #df = encode_df(df)
    #df_x, df_y = split_data(12, 4, df)
    #y_shift = shift_y(df_y)
    #df_x = df_x.reshape(1, 12, 10)
    #y_shift = y_shift.reshape(1, 4, 10)
    #df_y = df_y.reshape(1, 4, 10)
    #models.train_model.summary()
    #train(models.train_model, df_x, y_shift, df_y)