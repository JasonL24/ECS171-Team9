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

const MIDIjs = window.MIDIjs;

const Song = () => { 
  var barProgress = 0;
  const [isPaused, setIsPaused] = useState(false);
  const [progress, setProgress] = useState(0);
  const [timerStarted, setTimerStarted] = useState(false);
  const song = useSelector(state => state.song.song)
  const dispatch = useDispatch();

  useEffect(() => {
    // const song_id = window.location.pathname.split('/')[2]
    const song_id = '94ba49' // temporary hard coding
    dispatch(fetchSong(song_id));
    const location = './ml_src/midi_song/' + song_id + '.mid';
    firebasegs.child(location).getDownloadURL().then(function(url) {
      console.log(url);
      //MIDIjs.play('../../../../backend/ml_src/midi_song/358ee2.mid');
    });
  }, [])

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
  var time = Number(Math.floor(time))
  var minutes = Math.floor(time / 60);
  var seconds = time - minutes * 60;

  if (seconds < 10) {
    seconds = `0${seconds}`;
  }

  return `${minutes}:${seconds}`;
}

export default Song;
