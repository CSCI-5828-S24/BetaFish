import React, { useState } from 'react';
import './App.css';
import Search from './search/Search';
import { GlobalState } from './types';


function App() {

  const [globalState, setGlobalState] = useState<GlobalState>({
    filters: {
      long: null,
      lat: null,
      startDate: new Date().toJSON().slice(0, 10),
      endDate: new Date().toJSON().slice(0, 10)
    },
    crimeList: {
      page_no: 1,
      page_size: 10,
      data: []
    }
  });

  return (
    <div className="App">
      <Search globalState={globalState} setGlobalState={setGlobalState}/>
    </div>
  );
}

export default App;
