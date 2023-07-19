import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import Recommendations from './Recommendations';
import AddData from './AddData';

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/recommendations">Recommendations</Link>
            </li>
            <li>
              <Link to="/addData">Add Data</Link>
            </li>
          </ul>
        </nav>

        <Route exact path="/recommendations" component={Recommendations} />
        <Route exact path="/addData" component={AddData} />
      </div>
    </Router>
  );
}

export default App;
