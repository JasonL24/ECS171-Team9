import numpy as np
import pandas as pd
from math import ceil
import os
import pretty_midi
import py_midicsv as pm

midi_dir = './local_MIDI/'
parsed_dir = 'modern/'


for filename in os.listdir(midi_dir):
    _filename = os.path.splittext(filename)[0]
    print(_filename)


string = ''
for line in data:
    string += '%f %d %d' % (line[0], line[1], line[2])
    string += '\n'


midi_object = pm.csv_to_midi(string)

with open("alb_esp1.mid", "wb") as output_file:
    midi_writer = pm.FileWriter(output_file)
    midi_writer.write(midi_object)