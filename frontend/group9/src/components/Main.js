import React from 'react';
import { Link } from 'react-router-dom';


const Main = () => {
  return(
    <div>
      <Link to="/library" >
        <button>Library</button>
      </Link>
    </div>
  )
}

export default Main;
