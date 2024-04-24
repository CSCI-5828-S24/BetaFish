import { GlobalStateProps } from "../../types";

import "./CrimeListSection.css"

const CrimeListSection = (props: GlobalStateProps) => {
    return (
        <div className="CrimeList">
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
            props.globalState.crimeList.data.map((item) => {
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
    );
}

export default CrimeListSection;