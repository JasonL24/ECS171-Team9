import backend from '../api/backend';
import { FETCH_LIBRARY } from './types';

export const fetchLibrary = () => async (dispatch) => {
  const res = await backend.get('/api/library');
  dispatch({type: FETCH_LIBRARY, payload: res.data })
};