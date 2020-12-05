import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Button from '@material-ui/core/Button';
import './Main.css';
import backend from '../api/backend';
import Navbar from './Navbar';
import Loading from './Loading';

const Main = () => {
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const generateSong = async () => {
    setIsLoading(true);
    const res = await backend.get('/api/generate');
    if (res.data) {
      setResponse(res.data);
      setIsLoading(false);  
    }
  }


  const renderAll = () => {
    if (isLoading) {
      return (<Loading />)
    } else if (response === null) {
      return (
        <div>
          <Navbar />
          <div class="main-center-container">
            <div class="main-text-container">
              <div class="main-center-title">MusicSynth</div>
              <div class="main-center-subtitle">AI that makes music for you</div>
            </div>  
            <Button class="main-generate-button" color="primary" size="large" onClick={() => generateSong()}>Generate!</Button>
          </div>
        </div>
      );
    } else {
      const destination = '/song/' + response.song_id;
      return (<Link to={destination} className="song-complete">
        <Button color="primary" size="large" variant="contained">Song Complete. Listen now!</Button>
      </Link>);
    }
  }
  return(
    <div>
      {renderAll()}
    </div>
  )
}

export default Main;
