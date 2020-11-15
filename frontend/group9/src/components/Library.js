import React, {useEffect} from 'react';
import { useDispatch, useSelector } from 'react-redux';
import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';
import Helmet from 'react-helmet';

import './Library.css';
import { fetchLibrary } from '../actions';
import Navbar from './Navbar';

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
          <div>
            <Helmet>
              <style>{'body { background-color: #fff3b6 }'}</style>
            </Helmet>
            <Container maxWidth="lg">
              <li className="song-item">
                <p className="flex-item-size">{song.name} </p>
                <p className="flex-item-size">{song.genre}</p>
                <p className="flex-item-size">{song.duration}</p>
                <p className="flex-item-size">{song.bars} bars</p>
                <p className="flex-item-size">{song.rating}/10</p>
                <p className="flex-item-size">{song.likes} People Liked it </p> 
                <Button className="flex-item-size" color="primary">Play</Button> 
              </li>
            </Container>
          </div>
        )
      })
    )
  }
  return(
    <div className="page-font">
      <Navbar />
      <h1 className="library-title">Music Library</h1>
      <Container maxWidth="lg" className="titles-bolder">
        <li className="song-item">
          <p className="flex-item-size">Name</p>
          <p className="flex-item-size">Genre</p>
          <p className="flex-item-size">Time Length</p>
          <p className="flex-item-size"># of Bars</p>
          <p className="flex-item-size">Score</p>
          <p className="flex-item-size">Likes</p> 
          <p className="button-title">Button</p>
        </li>
      </Container>
      <ul className="song-list-container">
        {renderSongs()}
      </ul>
    </div>
  )
}

export default Library;
