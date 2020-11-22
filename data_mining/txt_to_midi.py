import os
import pretty_midi

txt_dir = 'txt_dir/'
newMidi_dir = './newMidi/'
delta = 0.07

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
    song.write(newMidi_dir + _filename + '.mid')
