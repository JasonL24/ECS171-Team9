# ECS 171 Group 9: Music Synth
Composing music is hard, especially for people who have no experience in the field of music. 
Therefore, we came up with the idea to let computers compose music for us. The project is to create a web application 
that uses our machine learning algorithm to generate simple music melodies. The user can specify the theme of their music, 
and give ratings based on the music generated.

## How to Run Locally
### Necessary installations
* Node.js and npm (https://nodejs.org/en/)
* Python 3.5 - 3.8 (https://www.python.org/downloads/)  NOTE: Python 3.9 causes Tensorflow error
* venv (run `pip install virtualenv` in terminal/command prompt)

#### Step 1 - Clone Repo
Clone the repo into your local machine
`git clone https://github.com/JasonL24/ECS171-Team9.git` or SSH clone if you have an SSH key setup.

#### Step 2 - Backend Setup
* We sent an email about the Firebase credentials. The `ecs171group9-a231f0136e76.json` file we sent must be placed in the `/backend/ml_src` directory.
* Change into the `\ECS171Group9\backend` directory.
* Create Virtual Environment with `python -m venv env`.
* Activate the Virtual Environment - you should see (env) appear before your pwd in your terminal/command prompt after completing this step.
   * For Mac: Run `source env/bin/activate`
   * For PC: Run `env\Scripts\activate`
* Run `pip install -r requirements.txt` to install dependencies (this may take a couple minutes). 
* Run `python run.py` to start the server.
* You may see some tensorflow warnings but you should eventually see a message saying `Running on http://127.0.0.1:5000/`
* Visit *http://localhost:5000/api/test* in your browser to make sure you can see the test message.

The backend is set up now!

#### Step 3 - Frontend Setup
* In the Firebase email we also sent `firebase.js`. That file should be placed in `/frontend/group9/src`.
* Open up a new separate terminal
* Change into the `ECS171Group9\frontend\group9` directory.
* Run `npm install` to install the dependencies (this may take a minute or two).
* Run `npm start`. It should open *http://localhost:3000/* in your browser.

The frontend is set up now!

### Running the App in General
To shut down the frontend or backend server type *ctrl* + *C* in the command prompt (*command* + *C* in terminal for Mac).

To start the frontend server again run `npm start` in the `fontend/group9` directory.
To start the backend server again run `python run.py` in the `/backend` directory.


##### Questions/Concerns
If you have any questions or problems setting up the local environment, ask in the `software-e` channel on Discord or ask Jason or Haoston personally.
