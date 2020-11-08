from music21 import *
import os
import pretty_midi

##midi_source = './local_MIDI'
##
##for midi_ in os.listdir(midi_source):
##    path = os.path.join(midi_source, midi_)
##
##    mf = midi.MidiFile()
##    mf.open(path)
##
##    """do stuff here lol"""
##
##    mf.read()
##    mf.close()

import pretty_midi
# Load MIDI file into PrettyMIDI object
midi_data = pretty_midi.PrettyMIDI('Test.mid')
# Print an empirical estimate of its global tempo
print(midi_data.estimate_tempo())
# Compute the relative amount of each semitone across the entire song, a proxy for key
total_velocity = sum(sum(midi_data.get_chroma()))
print([sum(semitone)/total_velocity for semitone in midi_data.get_chroma()])
# Shift all notes up by 5 semitones
print(midi_data.instruments)
##for instrument in midi_data.instruments:
##    # Don't want to shift drum notes
##    if not instrument.is_drum:
##        for note in instrument.notes:
##            note.pitch += 5
### Synthesize the resulting MIDI data using sine waves
##audio_data = midi_data.synthesize()

f = open("parsedMidi.txt", "w")
for instrument in midi_data.instruments:
    print(instrument.name)
    f.write( "\n" +str(instrument.name) )
    for i,note in enumerate(instrument.notes):
        print(note)
        f.write( "\n" +str(note))
        if (i>5):
            break

f.close()


