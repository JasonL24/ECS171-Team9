from models.utils import *
from models.music_nn import *

models = MusicNN()
models.load_weights('./trained_models/big_set')


def generate_song(length: int = 30):
    if not length:
        length = random_length()

    enc, dec = generate_sequences()  # ('3')
    song = models.generate_songs(enc, dec, length)
    song = song_threshold(song)
    return decode_song(song, '0')


def song_to_txt(song, length):
    dt = np.linspace(0, 0.07 * length, length + 1)
    dt = np.delete(dt, -1).reshape((1, -1))
    notes = np.array(song)
    song_list = np.concatenate([dt, notes]).transpose()

    with open('new_song.txt', 'w')as f:
        f.write('"New Song"\n\n')
        f.write('# Piano right\n')
        for i in range(length):
            time, pitch, vel = song_list[i, :]
            string = '%.6f %d %d\n' % (time, pitch, vel)
            f.write(string)

    return song_list


if __name__ == '__main__':
    pitches, velocities = generate_song(100)
    song_to_txt([pitches, velocities], 100)
