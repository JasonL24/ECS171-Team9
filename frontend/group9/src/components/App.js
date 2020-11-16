import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import Main from './Main';
import Library from './Library';
import Song from './Song';
import About from './About';

const App = () => {
  return (
    <div>
      <Router>
        <Route path="/" exact component={Main} />
        <Route path="/library" component={Library} />
        <Route path ="/song" component={Song} />
        <Route path ="/about" component={About} />
      </Router>
    </div>
  )
}

export default App;
