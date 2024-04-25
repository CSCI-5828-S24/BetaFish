import { GlobalStateProps } from "../../types";

import "./CrimeListSection.css"

const CrimeListSection = (props: GlobalStateProps) => {

    const clickHandler = (pair: [number, number]) => {
      // window.scrollTo(0,0)
      props.setGlobalState(prev => {
        return {
          ...prev,
          map: {
            lat: pair[0],
            long: pair[1]
          }
        }
      })
    }
  
    return (
      <div className="CrimeList">
        <table>
          <thead>
            <tr className="headerrow">
              <th>Incident ID</th>
              <th>Offense Type</th>
              <th>Incident Address</th>
              <th>Reported On</th>
              <th>Victims</th>
            </tr>
          </thead>
          <tbody>
          {
            props.globalState.crimeList.data.length > 0?
              props.globalState.crimeList.data.map((item) => {
                  return (
                    <tr className="datarow" key={item["OBJECTID"]} onClick={clickHandler.bind(null, [parseFloat(item["GEO_LAT"]), parseFloat(item["GEO_LON"])])}>
                      <td className="datacell">{item["INCIDENT_ID"]}</td>
                      <td className="datacell">{item["OFFENSE_TYPE_ID"]}</td>
                      <td className="datacell">{item["INCIDENT_ADDRESS"].trim()}</td>
                      <td className="datacell">{new Date(parseInt(item["REPORTED_DATE"])).toLocaleDateString()}</td>
                      <td className="datacell">{item["VICTIM_COUNT"]}</td>
                    </tr>
                  );
                }
              ):
              <tr className="datarow">
                <td className="datacell">-</td>
                <td className="datacell">-</td>
                <td className="datacell">-</td>
                <td className="datacell">-</td>
                <td className="datacell">-</td>
              </tr>
          }
          </tbody>
        </table>
      </div>
    );
}

export default CrimeListSection;