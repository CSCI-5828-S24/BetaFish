import { GlobalStateProps } from "./types";

const getAllData = (props: GlobalStateProps) => {
    fetch(`/api/alldata`)
      .then(response => response.json())
      .then(json => {
        console.log(json["data"])
        props.setGlobalState({
            ...props.globalState,
            crimeList: json["data"]
        })
      })
      .catch(error => console.log(error));
}

export { getAllData }