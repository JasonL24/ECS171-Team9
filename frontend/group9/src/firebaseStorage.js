import firebase from 'firebase';

var storage = firebase.storage()

var firebasegs = storage.refFromURL('gs://ecs171group9.appspot.com');

const getSongURL = (song_id) => {
  firebasegs.child('./ml_src/midi_song').then(function(url))
  
}

export default firebasegs;
