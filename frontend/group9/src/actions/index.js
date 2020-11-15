import { FETCH_LIBRARY } from './types';
import firebase from '../firebase';
var library = null;

var ref = firebase.database().ref();
ref.once('value',(snap)=>{
    console.log(snap.child('library').val());
  });

export const fetchLibrary = () => async (dispatch) => {
  // const res = await database.ref().child('library');
  // console.log(res);
  //dispatch({type: FETCH_LIBRARY, payload: res.data })
};