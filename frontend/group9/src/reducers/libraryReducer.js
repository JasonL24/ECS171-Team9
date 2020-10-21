import { FETCH_LIBRARY } from '../actions/types';

const INITAL_STATE = {
  songs: []
}

export default (state = INITAL_STATE, action) => {
  switch (action.type) {
    case FETCH_LIBRARY:
      state.songs = action.payload;
      return {...state};
    default:
      return state;
  }
}