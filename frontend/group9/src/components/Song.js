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
  const [progress, setProgress] = useState(0);
  const [song_loc, setSongLoc] = useState(false);
  const [duration, setDuration] = useState(0);
  var dur = null;
  const song = useSelector(state => state.song.song)
  const dispatch = useDispatch();

  useEffect(() => {
    const song_id = window.location.pathname.split('/')[2]
    dispatch(fetchSong(song_id));
    const location = './ml_src/midi_song/' + song_id + '.mid';
    firebasegs.child(location).getDownloadURL().then(function(url) {
      console.log(url);
    });
    const songLocation = '../midi/' + song_id +'.mid';
    setSongLoc('../midi/' + song_id +'.mid');
    console.log("CHECK", songLocation)
    MIDIjs.get_duration(songLocation, function(seconds) { 
      console.log("length", seconds);
      setDuration((old) => seconds);
      dur = seconds;
    } );
    MIDIjs.play(songLocation);
    console.log(MIDIjs)
    function doTimer(ev) {
      if (ev.time <= Math.ceil(dur)) {
        setProgress(() => ev.time);
      }
    }
    MIDIjs.player_callback = doTimer;
  }, [])



  const playSong = () => {
    console.log(song_loc);
    if (Math.ceil(duration) === Math.ceil(progress)) {
      MIDIjs.play(song_loc)
    } else {
      MIDIjs.resume();
    }
  }

  const pauseSong = () => {
    MIDIjs.pause();
  }

  const renderSong = () => {
    return (
      <div className="single-song">
        <div className="song-title">
          Song ID: {song.song_id}
        </div>
        <div className="song-genres">
          Genre: {song.genres}
        </div>
      </div>
    )
  }

  return (
    <div>
      <Navbar />
      <div className="song-area">
        <div className="title-row">
          {renderSong()}
          <a href={song_loc} download={song_loc}>
            <Button variant="contained" color="primary">
              Download MIDI
            </Button>
          </a>
        </div>
        <LinearProgress color="primary" variant="determinate" value={progress/duration}/>
        <div className="progress-row">
          <div className="play-pause">
            <Button variant="outlined" color="primary" onClick={() => playSong()}>
              <PlayArrowIcon/>
            </Button>
            <Button variant="outlined" color="primary" onClick={() => pauseSong()}>
              <PauseIcon/>
            </Button>
          </div>
          <h4>{minSecForm(progress)} / {minSecForm(duration)}</h4>
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
