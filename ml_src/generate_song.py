import pretty_midi
from models.utils import *
from models.music_nn import *
from firebase_admin import credentials, initialize_app, storage

models = MusicNN()
models.load_weights('./trained_models/duration')
txt_dir = './txt_song/'
newMidi_dir = './midi_song/'
n = '4'


def generate_song():
    durations, pitches, velocities = _get_sequence(90)
    _song_to_txt([durations, pitches, velocities], 90)
    _duration_to_midi()
    # _txt_to_mid()

    # # Init firebase with your credentials
    # cred = credentials.Certificate('../frontend/group9/src/firebase.js')
    # initialize_app(cred, {'storageBucket': 'ecs171group9.appspot.com'})
    #
    # # Put your local file path
    # file_name = "myImage.jpg"
    # bucket = storage.bucket()
    # blob = bucket.blob(file_name)
    # blob.upload_from_filename(file_name)
    #
    # # Opt : if you want to make public access from the URL
    # blob.make_public()
    #
    # print("your file url", blob.public_url)


def _get_sequence(length: int = 30):
    if not length:
        length = random_length()

    # enc, dec = better_seq(n)  # ('3')
    enc, dec = generate_sequences()  # ('3')
    _song = models.generate_songs(enc, dec, length)
    _song = song_threshold(_song)
    return decode_song(_song, n)


def _song_to_txt(_song, length):
    _song = np.array(_song)
    with open('./txt_song/new_song.txt', 'w')as f:
        f.write('"New Song"\n\n')
        f.write('# Piano right\n')
        for i in range(length):
            duration, pitch, vel = _song[:, i]
            string = '%.6f %d %d\n' % (duration, pitch, vel)
            f.write(string)


def _duration_to_midi():
    for filename in os.listdir(txt_dir):
        _filename = os.path.splitext(filename)[0]
        song = pretty_midi.PrettyMIDI()
        ptr = 0
        with open(txt_dir + filename, 'r') as f:
            for line in f:
                if line[0] == '"' or line == '\n':
                    continue  # song name
                elif line[0] == '#':
                    instrument_program = pretty_midi.instrument_name_to_program("acoustic grand piano")
                    inst = pretty_midi.Instrument(program=instrument_program)
                else:
                    line = line.split()
                    if line[1] == line[2] == '0':
                        ptr += float(line[0])
                    else:
                        note = pretty_midi.Note(start=ptr, end=ptr + float(line[0]), pitch=int(line[1]),
                                                velocity=int(line[2]))
                        inst.notes.append(note)
                        ptr += float(line[0])
        song.instruments.append(inst)
        song.write(newMidi_dir + _filename + '.mid')


if __name__ == '__main__':
    generate_song()
