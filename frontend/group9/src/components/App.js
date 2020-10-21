import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import Main from './Main';
import Library from './Library';
const App = () => {
  return (
    <div>
      <Router>
        <Route path="/" exact component={Main} />
        <Route path="/library" component={Library} />
      </Router>
    </div>
  )
}

export default App;
