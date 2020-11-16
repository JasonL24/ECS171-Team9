import React from 'react';
import Helmet from 'react-helmet';
import { Link } from 'react-router-dom';
import Button from '@material-ui/core/Button';
import './Navbar.css';

const Navbar = () => {

  return(
    <div>
      <Helmet>
        <style>{'body { background-color: #fff3b6 }'}</style>
      </Helmet>
      <div className="navbar-container">
        <div>MusicSynth</div>
        <Link to="/" style={{ textDecoration: 'none' }}>
          <Button class="navbar-titles">Home</Button>
        </Link>
        <Link to="/about" style={{ textDecoration: 'none' }}>
          <Button class="navbar-titles">About</Button>
        </Link>
        <Link to="/library" style={{ textDecoration: 'none' }}>    
          <Button class="navbar-titles">Library</Button>
        </Link>
      </div>
    </div>
  )
}

export default Navbar;
