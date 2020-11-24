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

Then you need the tensorflow addons package
- `pip install tensorflow-addons` This one has no Annaconda equivalent.

## Troubleshooting
Some common errors and their solutions.

1. Fails to import tensorflow_addons
- Go to this Stackoverflow https://stackoverflow.com/questions/62696815/tensorflow-core-api-v2-random-has-no-attribute-generator
