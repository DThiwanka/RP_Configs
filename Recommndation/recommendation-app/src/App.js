import React from 'react';
import { BrowserRouter as Router, Link, Route, Switch } from 'react-router-dom';
import Recommendations from './components/Recommendations';
import Home from './components/Home';
import './App.css';


function App() {
  return (
    <Router>
      <nav className="navbar">
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/recommendations">Recommendations</Link>
          </li>
        </ul>
      </nav>

      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/recommendations" component={Recommendations} />
      </Switch>
    </Router>
  );
}

export default App;
