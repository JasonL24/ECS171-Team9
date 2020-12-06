# How to: Data Mine
The first thing is you never upload any data to GitHub (etc MID files). GitHub only supports up to about 1 GB of storage.
So it is probably not idea to upload everything to GitHub.

Remeber to check the drive and see if someone has parsed a song before upload. Repeated data set could make the NN model
biased. It is generally not healthy. You can however upload .txt files (parsed MIDI songs) up to GitHub.
We will deal with the parsed data set once it gets too big.



## Installation
Here are a few pacakges you are going to need right now (Will update as we go).

1. `pip install music21`
1. `pip install pretty_midi`

## File Structure
Since we will be opening files in folders. It will probably be easier if we use similar file structure so we can have
matching relative path.

ECS 171 Group 9 <br />
├───data_mining <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├───local_MIDI <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├──song1.mid <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──song2.mid <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├───parsed_data <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├──song1.txt <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──song2.txt <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└───README.md <br />


## How to Parse your Midi files
piano_music and piano_parsed are two folders you must create in the same
directory as your midi_process python file.

piano_music contains all of the midi files you would like to parse. Then
you run the python file and it will parse each song and create new files
for each in the piano_parsed folder.


## How to Read Parsed Notes
Here is an example of what you might see in the parsed data

```
"alb_esp1"

#  Piano right
0.32110 0 0
0.32110 81 60
1.93255 88 66
0.06667 86 55
0.06667 88 47
0.26318 86 62

```
The first line is the name of the file so just skip it unless you want to
keep track for error checking

The third line is the instument. All intruments are denoted by # at the
front of the line

The following lines are the duration of the note followed by pitch and
velocity for each note played by the instument for the rest of the song.

Other instuments in the song will similarly have their own # intrument name
and then have their notes starting from the start of the song to the end. 



## How to recreate your Midi files from txt files
txt_dir and newMidi are two folders you must create in the same
directory as your txt_to_midi python file.

txt_dir contains all of the text files you would like to turn into midi
files. Then you run the python file and it will go through each note,
create a song object, and append the notes to the song object. They will
then be formated into a valid midi file and put into the newMidi folder,
one file per song/text file. 
