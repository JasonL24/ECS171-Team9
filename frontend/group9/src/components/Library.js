import React, {useEffect} from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { fetchLibrary } from '../actions';

const Library = () => {
  // Fetch library on mount
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(fetchLibrary());
  }, []);

  const librarySongs = useSelector(state => state.library.songs)


  const renderSongs = () => {
    return (
      librarySongs.map(song => {
        return (
          <li>{song}</li>
        )
      })
    )
  }
  return(
    <div>
      <ul>
        {renderSongs()}
      </ul>
    </div>
  )
}

export default Library;
