from music21 import *
import os

midi_source = './local_MIDI'

for midi_ in os.listdir(midi_source):
    path = os.path.join(midi_source, midi_)

    mf = midi.MidiFile()
    mf.open(path)

    """do stuff here lol"""

    mf.read()
    mf.close()

