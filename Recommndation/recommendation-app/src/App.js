import React from 'react';
import { BrowserRouter as Router, Link, Route, Switch } from 'react-router-dom';
import Recommendations from './components/Recommendations';
import Home from './components/Home';
import DataInputForm from './components/DataInputForm';
import OutfitSelector from './components/OutfitSelector';
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
          <li>
            <Link to="/DataInput">DataInput</Link>
          </li>
          <li>
            <Link to="/outfit">Outfit</Link>
          </li>
        </ul>
      </nav>

      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/recommendations" component={Recommendations} />
        <Route path="/DataInput" component={DataInputForm} />
        <Route path="/outfit" component={OutfitSelector} />
      </Switch>
    </Router>
  );
}

export default App;
