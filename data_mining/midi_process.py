import numpy as np
import pandas as pd
from math import ceil
import os
import pretty_midi

midi_dir = './local_MIDI/'
parsed_dir = 'modern/'
delta = 0.07

for filename in os.listdir(midi_dir):
    _filename = os.path.splitext(filename)[0]
    print(_filename)

    # Code to help quicken the parsing process
    # if (_filename[0] == '2' or _filename[0] == 'A' or _filename[0] == 'a'):
    #    continue
    
    midi_data = pretty_midi.PrettyMIDI(midi_dir + filename)

    with open(parsed_dir + _filename + '.txt', "w") as f:
        #print(_filename)
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
                string += '%f %d %d' % (line[0], line[1], line[2])
                string += '\n'

            f.write(string)
