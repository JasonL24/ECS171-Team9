import React from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';

import './Loading.css';
const Loading = () => {
  return(
    <div className="loader">
      <h1>GENERATING SONG...</h1>
      <CircularProgress />
      <div className="process-info">
        This process should take 10-20 seconds
      </div>
    </div>
  )
}

export default Loading;
