import React, {useState, useEffect} from 'react';
import { useDispatch, useSelector } from 'react-redux';
import Button from '@material-ui/core/Button';
import PlayArrowIcon from '@material-ui/icons/PlayArrow';
import PauseIcon from '@material-ui/icons/Pause';
import LinearProgress from '@material-ui/core/LinearProgress';

import { fetchSong } from '../actions';
import firebasegs from '../firebaseStorage';
import './Song.css';
import Navbar from './Navbar';

const Song = () => { 
  var barProgress = 0;
  const [progress, setProgress] = useState(0);
  const [timerStarted, setTimerStarted] = useState(false);
  const song = useSelector(state => state.song.song)
  const dispatch = useDispatch();
  var audioElement = document.getElementsByTagName("audio")[0]
  

  useEffect(() => {
    // const song_id = window.location.pathname.split('/')[2]
    const song_id = '94ba49' // temporary hard coding
    dispatch(fetchSong(song_id));
    const location = './ml_src/midi_song/' + song_id + '.mid';
    firebasegs.child(location).getDownloadURL().then(function(url) {
      console.log(url);
    });
    audioElement.src = '../0b9d60.wav';
  }, [])

  const doTimer = () => {
    if (!timerStarted) {
      setInterval(() => {
        console.log(audioElement.currentTime)
        setProgress(() => audioElement.currentTime);
      }, 1000);
      setTimerStarted(true);
    }
  }

  const playSong = () => {
    console.log(audioElement);
    audioElement.play();
  }

  const pauseSong = () => {
    audioElement.pause();
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
  var time = Number(Math.floor(time));
  var minutes = Math.floor(time / 60);
  var seconds = time - minutes * 60;

  if (seconds < 10) {
    seconds = `0${seconds}`;
  }

  return `${minutes}:${seconds}`;
}

export default Song;
