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
      lat: 39.74956044238265,
      long: -104.95078325271608,
      startDate: new Date().toJSON().slice(0, 10),
      endDate: new Date().toJSON().slice(0, 10)
    },
    map: {
        lat: 39.74956044238265,
        long: -104.95078325271608
    },
    crimeList: {
      page_no: 1,
      page_size: 20,
      data: []
    },
    crimeTotals: {
      data: []
    },
    analytics: {
      freq: {
        labels: [],
        datasets: [
          {
            label: 'Crime Frequency',
            data:  [],
            borderColor: '#ff936c',
            backgroundColor: '#ff936c'
          }
        ]
      },
      totals: {
        labels: [],
        datasets: [
          {
            label: 'Crime Totals',
            data: [],
            borderColor: '#ff936c',
            backgroundColor: '#ff936c',
          }
        ],
      },
    }
  });


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
