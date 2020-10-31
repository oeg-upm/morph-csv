import React from 'react';
import './App.css';
import 'antd/dist/antd.css'; // or 'antd/dist/antd.less'
import {Route, Switch,BrowserRouter} from 'react-router-dom'
import Home from './pages/Home';
function App() {
  return (
    <BrowserRouter>
    <Switch>
    <Route path="/" component={Home}/>  
    </Switch>
    </BrowserRouter>
  );
}

export default App;
