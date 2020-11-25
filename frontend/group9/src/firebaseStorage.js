import firebase from 'firebase';

var storage = firebase.storage()

var firebasegs = storage.refFromURL('gs://ecs171group9.appspot.com');

export default firebasegs;
