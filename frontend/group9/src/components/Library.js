import React, {useEffect} from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
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
    console.log("Render log", librarySongs);
    return (
      librarySongs.map(song => {
        return (
          <div id={song.song_id}>
            <Helmet>
              <style>{'body { background-color: #fff3b6 }'}</style>
            </Helmet>
            <Container maxWidth="lg">
              <li className="song-item">
                <p className="flex-item-val">{song.song_id}</p>
                <p className="flex-item-val">{song.genres}</p>
                <p className="flex-item-val">{Math.floor(song.duration)} sec</p>
                <Link className="flex-item-val" to={`/song/${song.song_id}`}>
                  <Button color="primary">Play</Button>
                </Link>
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
          <p className="flex-item-size">Song ID</p>
          <p className="flex-item-size">Genre</p>
          <p className="flex-item-size">Time Length</p>
          <p className="button-title">Play Song</p>
        </li>
      </Container>
      <ul className="song-list-container">
        {renderSongs()}
      </ul>
    </div>
  )
}

export default Library;
