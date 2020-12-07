# How to: Machine Learning
Here is the guide to setup the ML environment. The current setup is very rudimentary and does not require a GPU.

I strongly recommending using Annaconda. It helps you manage different package and version. You could have a lot of internal
packaging version conflicts without them.

## Installation
Here are a few packages you are going to need right now (Will update as we go).

If you DO NOT have a dedicated graphics card (GPU), use the first option. If you DO have a dedicated GPU
use command two. 
-  `pip install tensorflow` Alternatively, if you are using Annaconda  `conda install tensorflow`
-  `pip install tensorflow-gpu` or `conda install tensorflow-gpu`
-  `pip install numpy pandas scikit-learn`

## File Documentations
All the important files are written in python. There is one source folder (models) and two machine learning files.

- *keras_train.py* 

This the main file for training the model. It calls the on the fit function repetitively until the user pauses it with
ctrl + c. Check the keras_train.py for the whole command line argument cheatsheet. Here is an example command.

`python keras_train.py model=load_model@./trained_models/duration save_model_to=./trained_models/duration data=generate@1 epoch=30 `


- *generate_song.py*
This is the main inference model where is reads the saved model and create the song. Here is an example command.

`python generate_song.py`

- *modle


