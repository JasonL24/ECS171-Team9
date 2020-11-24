import pretty_midi
from .models.utils import *
from .models.music_nn import *
from . import *
from firebase_admin import storage
import uuid

delta = 0.07
models = MusicNN()

models.load_weights('./ml_src/trained_models/big_set')
txt_dir = './ml_src/txt_song/'
newMidi_dir = './ml_src/midi_song/'
song_id = str(uuid.uuid1())[0:6]

def generate_song():
    song_length = 100
    pitches, velocities = _get_sequence(song_length)
    _song_to_txt([pitches, velocities], song_length)
    _txt_to_mid()

    # Init firebase with your credentials
    file_name = newMidi_dir + song_id + '.mid'
    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)

    # Opt : if you want to make public access from the URL
    blob.make_public()

    song_obj = {
        'name': "Temporary name",
        'duration': str(song_length * .07),
        'song_id': song_id,
        'genres': "Classical"
    }
    url = 'Library/' + song_id
    res = fb.patch(url, song_obj)
    print(res)

    return song_id


def _get_sequence(length: int = 30):
    if not length:
        length = random_length()

    # enc, dec = generate_sequences()
    enc, dec = better_seq(n)
    _song = models.generate_songs(enc, dec, length)
    _song = song_threshold(_song)
    return decode_song(_song, n)


def _song_to_txt(_song, length):
    dt = np.linspace(0, 0.07 * length, length + 1)
    dt = np.delete(dt, -1).reshape((1, -1))
    notes = np.array(_song)
    song_list = np.concatenate([dt, notes]).transpose()

    with open('./ml_src/txt_song/new_song.txt', 'w')as f:
        f.write('"New Song"\n\n')
        f.write('# Piano right\n')
        for i in range(length):
            time, pitch, vel = song_list[i, :]
            string = '%.6f %d %d\n' % (time, pitch, vel)
            f.write(string)

    return song_list


def _txt_to_mid():
    for filename in os.listdir(txt_dir):
        _filename = os.path.splitext(filename)[0]
        print(_filename)

        file = open(txt_dir + filename, 'r')
        lines = file.readlines()

        # Create a PrettyMIDI object
        song = pretty_midi.PrettyMIDI()
        instrument_program = pretty_midi.instrument_name_to_program('Cello')
        current_inst = pretty_midi.Instrument(program=instrument_program)

        # Skip tyhe file name
        line_count = 0
        # track if we have an instrument already or not
        inst = 0
        # track last pitch
        currentPitch = 0
        currentVelocity = 0
        currentStartTime = 0
        currentEndTime = 0
        for line in lines:
            if line_count == 0:
                line_count += 1
                continue
            if '#' in line:
                if inst:
                    print("##")
                    print("appending insturment")
                    print("##")
                    song.instruments.append(current_inst)
                else:
                    inst = 1

                print("Instrument Found: " + line[2:-1])
                # Create an Instrument instance for the instrument
                if line[2:-1] == "Piano left":
                    instrument_program = pretty_midi.instrument_name_to_program("acoustic grand piano")
                elif line[2:-1] == "Piano right":
                    instrument_program = pretty_midi.instrument_name_to_program("acoustic grand piano")
                else:
                    instrument_program = pretty_midi.instrument_name_to_program(line[2:-1])
                current_inst = pretty_midi.Instrument(program=instrument_program)

            else:
                line = line.strip()
                token = line.split(' ')
                if token[0] == "":
                    print("skipping empty line")
                    continue
                print(token)

                endValue = float(float(token[0]) + delta)
                if int(token[1]) != currentPitch:
                    note = pretty_midi.Note(velocity=currentVelocity, pitch=currentPitch, start=currentStartTime,
                                            end=currentEndTime)
                    current_inst.notes.append(note)
                    currentStartTime = float(token[0])
                    currentPitch = int(token[1])
                    currentVelocity = int(token[2])
                else:
                    currentEndTime = endValue
        print("appending last instrument")
        song.instruments.append(current_inst)
        song.write(newMidi_dir + song_id + '.mid')


if __name__ == '__main__':
    generate_song()
