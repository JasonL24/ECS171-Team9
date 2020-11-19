from models.utils import *
from models.music_nn import *

enc, dec = generate_sequences()

models = MusicNN()
models.load_weights('./trained_models/big_set')
song = models.generate_songs(enc, dec, 900)
np_song = np.array(song)
pitches, velocities = song_threshold(np_song)
print(pitches)
print(velocities)
