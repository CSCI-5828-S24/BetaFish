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
      startDate: new Date().toJSON().slice(0, 10),
      endDate: new Date().toJSON().slice(0, 10)
    },
    crimeList: {
      page_no: 1,
      page_size: 10,
      data: []
    }
  });

  const handleDump = () => {
    getAllData({
      globalState: globalState,
      setGlobalState: setGlobalState
    })
  }
  console.log(globalState.crimeList)
  return (
    <div className="App">
      <Search globalState={globalState} setGlobalState={setGlobalState}/>
      <div className="DataDump">
        <button onClick={handleDump}>Database Dump</button>
        <table>
          <tr>
            <th>Offense Type</th>
            <th>Incident Address</th>
            <th>First Occurrence</th>
            <th>Crime?</th>
            <th>Traffic?</th>
            <th>Victims</th>
          </tr>
          {

            globalState.crimeList.data.map((item) => {
                return (
                  <tr id={item["OBJECTID"]}>
                    <td>{item["OFFENSE_TYPE_ID"]}</td>
                    <td>{item["INCIDENT_ADDRESS"]}</td>
                    <td>{new Date(parseInt(item["FIRST_OCCURRENCE_DATE"])).toLocaleDateString()}</td>
                    <td>{item["IS_CRIME"]}</td>
                    <td>{item["IS_TRAFFIC"]}</td>
                    <td>{item["VICTIM_COUNT"]}</td>
                  </tr>
                );
              }
            )
          }
        </table>
      </div>
    </div>
  );
}

export default App;
