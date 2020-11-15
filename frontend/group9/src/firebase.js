//import firebase from "firebase/app";
// import "firebase/auth";
// import "firebase/firestore";
import firebase from 'firebase';

var firebaseConfig = {
  apiKey: "AIzaSyAlWfdSZ7S-q13R5ukb4Tj_FFGLR9EKA2o",
  authDomain: "ecs171group9.firebaseapp.com",
  databaseURL: "https://ecs171group9.firebaseio.com",
  projectId: "ecs171group9",
  storageBucket: "ecs171group9.appspot.com",
  messagingSenderId: "322595765037",
  appId: "1:322595765037:web:6f63b16e1fbf87f17971a4",
  measurementId: "G-K9GWRT93TF"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

export default firebase;