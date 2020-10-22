import React, {useEffect} from 'react';
import { useDispatch, useSelector } from 'react-redux';

import './Library.css';
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
          <li className="song-item">
            <p>{song.name} </p>
            <p>{song.genre}</p>
            <p>{song.duration}</p>
            <p>{song.bars} bars</p>
            <p>{song.rating}/10</p>
            <p>{song.likes} People Liked it </p>  
          </li>
        )
      })
    )
  }
  return(
    <div>
      <h1>Music Library</h1>
      <ul>
        {renderSongs()}
      </ul>
    </div>
  )
}

export default Library;
