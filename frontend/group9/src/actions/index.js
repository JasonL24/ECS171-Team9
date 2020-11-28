import { FETCH_LIBRARY, FETCH_SONG } from './types';
import firebase from '../firebase';

var ref = firebase.database().ref();
// ref.once('value',(snap)=>{
//     console.log(snap.child('library').val());
//   });



export const fetchSong = (song_id) => async (dispatch) => {
  ref.once('value').then(function(snapshot) {
    const res = snapshot.child(`Library/${song_id}`).val();
    console.log("inner res", res)
    dispatch({type: FETCH_SONG, payload: res })
  });
};

export const fetchLibrary = () => async (dispatch) => {
  var res = null;
  ref.once('value',(snap)=>{
    res = snap.child(`Library`).val();
    const libraryEntries = Object.values(res);
    console.log(libraryEntries);
    dispatch({type: FETCH_LIBRARY, payload: libraryEntries })

  });
};