import React, {useState} from 'react';
import { Link } from 'react-router-dom';
import Button from '@material-ui/core/Button';
import PlayArrowIcon from '@material-ui/icons/PlayArrow';
import PauseIcon from '@material-ui/icons/Pause';
import LinearProgress from '@material-ui/core/LinearProgress';

import './Song.css';
import Navbar from './Navbar';

const MIDIjs = window.MIDIjs;

// default song for now
const song = {
  title: 'Down and Out',
  genres: 'Sad, Slow, Melancholy',
  duration: 84
}

const Song = () => { 
  var barProgress = 0;
  const [isPaused, setIsPaused] = useState(false);
  const [progress, setProgress] = useState(0);
  const [timerStarted, setTimerStarted] = useState(false);

  const doTimer = () => {
    if (!timerStarted) {
      setTimerStarted(true);
      setInterval(() => {
        if (!isPaused) {
          barProgress = (progress / song.duration) * 100;
          setProgress((oldProgress) => {
            if (oldProgress + 1 < song.duration && !isPaused) {
              return oldProgress + 1;
            } else {
              return oldProgress;
            }
          });
        }
      }, 1000);
    }
  }

  const playSong = () => {
    if (isPaused) {
      setIsPaused(oldStatus => !oldStatus);
      MIDIjs.resume();
    } else {
      MIDIjs.play('https://en.wikipedia.org/wiki/File:MIDI_sample.mid?qsrc=3044#file');
    }
  }

  const pauseSong = () => {
    setIsPaused(oldStatus => !oldStatus);
    MIDIjs.pause();
    console.log("PAUSED", isPaused);
  }

  const renderSong = () => {
    return (
      <div className="single-song">
        <div className="song-title">
          {song.title}
        </div>
        <div className="song-genres">
          {song.genres}
        </div>
      </div>
    )
  }

  return (
    <div>
      {doTimer()}
      <Navbar />
      <div className="song-area">
        <div className="title-row">
          {renderSong()}
          <Button variant="contained" color="primary">
            Download
          </Button>
        </div>
        <LinearProgress color="primary" variant="determinate" value={barProgress}/>
        <div className="progress-row">
          <div className="play-pause">
            <Button variant="outlined" color="primary" onClick={() => playSong()}>
              <PlayArrowIcon/>
            </Button>
            <Button variant="outlined" color="primary" onClick={() => pauseSong()}>
              <PauseIcon/>
            </Button>
          </div>
          <h4>{minSecForm(progress)} / {minSecForm(song.duration)}</h4>
        </div> 
      </div>
    </div>
  )
};

const minSecForm = (time) => {
  var minutes = Math.floor(time / 60);
  var seconds = time - minutes * 60;

  if (seconds < 10) {
    seconds = `0${seconds}`;
  }

  return `${minutes}:${seconds}`;
}

export default Song;
