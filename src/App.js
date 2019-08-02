import React from 'react';
import './App.css';
import BackgroundMap from './BackgroundMap.js'

function App() {
  return (
    <div
    style={{position: 'absolute', width: '100%',height: '100%'}}>
    <BackgroundMap/>
    </div>
  );
}

export default App;
