import { combineReducers } from 'redux';
import libraryReducer from './libraryReducer';
import songReducer from './songReducer';


export default combineReducers({
  library: libraryReducer,
  song: songReducer
});
