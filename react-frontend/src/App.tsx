import React, { useState } from 'react';
import './App.css';
import Search from './search/Search';
import { GlobalState } from './types';
import Header from './Header';
import Analytics from './analytics/Analytics';


function App() {

  const [globalState, setGlobalState] = useState<GlobalState>({
    active: "search",
    filters: {
      long: -105.2668960437206,
      lat: 40.00943069669764,
      startDate: new Date().toJSON().slice(0, 10),
      endDate: new Date().toJSON().slice(0, 10)
    },
    fetched: false,
    crimeList: {
      page_no: 1,
      page_size: 10,
      data: []
    }
  });

  console.log(globalState)

  return (
    <div className="App">
      <Header globalState={globalState} setGlobalState={setGlobalState} />
      <div id="SectionContainer">
        <Search globalState={globalState} setGlobalState={setGlobalState} />
        <Analytics globalState={globalState} setGlobalState={setGlobalState} />
      </div>
    </div>
  );
}

export default App;
