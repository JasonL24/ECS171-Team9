import numpy as np
import pandas as pd
from math import ceil
import os
import pretty_midi

midi_dir = './local_MIDI/'
parsed_dir = './parsed_data/'
delta = 0.07

for filename in os.listdir(midi_dir):
    _filename = os.path.splitext(filename)[0]
    midi_data = pretty_midi.PrettyMIDI(midi_dir + filename)

    # Print an empirical estimate of its global tempo
    # print(midi_data.estimate_tempo())

    # Compute the relative amount of each semitone across the entire song, a proxy for key
    # total_velocity = sum(sum(midi_data.get_chroma()))
    # print([sum(semitone) / total_velocity for semitone in midi_data.get_chroma()])

    # Shift all notes up by 5 semitones
    # print(midi_data.instruments)

    with open(parsed_dir + _filename + '.txt', "w") as f:
        print(_filename)
        f.write("\"" + _filename + "\"" + '\n\n')

        for instrument in midi_data.instruments:
            # print(instrument.name)
            f.write("# " + str(instrument.name) + '\n')

            song_length = instrument.notes[-1].end
            intervals = int(song_length / delta)
            time_stamp = np.linspace(0, intervals * delta, intervals + 1)
            data = np.zeros([intervals + 1, 3])
            data[:, 0] = time_stamp

            for note in instrument.notes:
                taken_spaces = int(note.duration / delta)  # calculate the space required for the duration
                ptr = ceil(note.start / delta)
                note = [note.pitch, note.velocity]
                if taken_spaces:
                    data[ptr: ptr + taken_spaces, 1:] = np.array([note, ] * taken_spaces)

            string = ''
            for line in data:
                string += ' '.join(['%.5f' % num for num in line])
                string += '\n'

            f.write(string)
