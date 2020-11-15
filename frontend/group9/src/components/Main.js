import React from 'react';
import { Link } from 'react-router-dom';
import Button from '@material-ui/core/Button';
import './Main.css';
import backend from '../api/backend';
import Navbar from './Navbar';

const Main = () => {
  const generateSong = async () => {
    const res = await backend.get('/api/generate');
    console.log(res);
  }

  return(
    <div>
      <Navbar />
      <div class="main-center-container">
        <div class="main-text-container">
          <div class="main-center-title">MusicSynth</div>
          <div class="main-center-subtitle">AI that makes music for you</div>
        </div>
        <Link to="/song" >
          <Button class="main-generate-button" color="primary" size="large" onClick={() => generateSong()}>Generate!</Button>
        </Link>
      </div>
    </div>
  )
}

export default Main;
