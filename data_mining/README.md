# How to: Data Mine
The first thing is you never upload any data to GitHub (etc MID files). GitHub only supports up to about 1 GB of storage.
So it is probably not idea to upload everything to GitHub.

Remeber to check the drive and see if someone has parsed a song before upload. Repeated data set could make the NN model
biased. It is generally not healthy.You can however upload .txt files (parsed MIDI songs) up to GitHub.
 We will deal with the parsed data set once it gets too big.



## Installation
Here are a few pacakges you are going to need right now (Will update as we go).

1. `pip install music21`

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


## How to Read Parsed Notes
Here are a list of conversion of the symbols used in parsed data

```
*  start of a note
&  end of a note
+  sharp
-  flat
0  rest
``` 
 