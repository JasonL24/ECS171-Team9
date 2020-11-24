import os
import pretty_midi

midi_dir = './local_MIDI/mozart/'
parsed_dir = './database/mozart/'

for filename in os.listdir(midi_dir):
    print(filename)
    _filename = os.path.splitext(filename)[0]
    midi_data = pretty_midi.PrettyMIDI(midi_dir + filename)

    with open(parsed_dir + _filename + '.txt', "w") as f:
        f.write("\"" + _filename + "\"" + '\n\n')
        for instrument in midi_data.instruments:
            if instrument.name == "Piano left" or instrument.name == "Piano right":
                song_length = len(instrument.notes)
                f.write('#  ' + str(instrument.name) + '\n')
                ptr = 0
                for note in instrument.notes:
                    # print(note)
                    if note.start > ptr:
                        duration = note.start - ptr
                        string = '%.5f %d %d\n' % (duration, 0, 0)
                        f.write(string)
                    duration = note.end - note.start
                    pitch = note.pitch
                    vel = note.velocity
                    string = '%0.5f %d %d\n' % (duration, pitch, vel)
                    f.write(string)
                    ptr = note.end
            else:
                continue
