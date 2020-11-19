from models.utils import *
from models.music_nn import *

models = MusicNN()
models.load_weights('./trained_models/big_set')


def generate_song(length: int = None):
    if not length:
        length = random_length()

    enc, dec = generate_sequences()
    song = models.generate_songs(enc, dec, length)
    np_song = np.array(song)
    return song_threshold(np_song)


if __name__ == '__main__':
    pitches, velocities = generate_song()
    print(pitches)
    print(velocities)
