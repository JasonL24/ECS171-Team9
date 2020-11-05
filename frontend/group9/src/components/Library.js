import React, {useEffect} from 'react';
import { useDispatch, useSelector } from 'react-redux';
import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';

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
          <Container maxWidth="md">
            <li className="song-item">
              <p>{song.name} </p>
              <p>{song.genre}</p>
              <p>{song.duration}</p>
              <p>{song.bars} bars</p>
              <p>{song.rating}/10</p>
              <p>{song.likes} People Liked it </p> 
              <Button color="primary">Play</Button> 
            </li>
          </Container>
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
