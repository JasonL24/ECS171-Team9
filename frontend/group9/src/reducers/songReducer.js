import { FETCH_SONG } from '../actions/types';

const INITAL_STATE = {
  song: {}
}

export default (state = INITAL_STATE, action) => {
  switch (action.type) {
    case FETCH_SONG:
      state.song = action.payload;
      return {...state};
    default:
      return state;
  }
}
