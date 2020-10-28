import React from 'react';
import { Link } from 'react-router-dom';
import Button from '@material-ui/core/Button';

const Main = () => {
  return(
    <div>
      <Link to="/library" >
        <Button color="primary" size="large">Library</Button>
      </Link>
    </div>
  )
}

export default Main;
