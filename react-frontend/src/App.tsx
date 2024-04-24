import React, { useState } from 'react';
import './App.css';
import Search from './search/Search';
import { GlobalState } from './types';
import { getAllData } from './api-interface';


function App() {

  const [globalState, setGlobalState] = useState<GlobalState>({
    filters: {
      long: null,
      lat: null,
      startDate: null,
      endDate: null
    },
    crimeList: []
  });

  const handleDump = () => {
    getAllData({
      globalState: globalState,
      setGlobalState: setGlobalState
    })
  }

  return (
    <div className="App">
      <Search globalState={globalState} setGlobalState={setGlobalState}/>
      <div className="DataDump">
        <button onClick={handleDump}>Database Dump</button>
        <pre id="dump">{JSON.stringify(globalState.crimeList, null, 2)}</pre>
      </div>
    </div>
  );
}

export default App;
