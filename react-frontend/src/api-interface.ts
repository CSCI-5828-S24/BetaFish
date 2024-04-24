import { GlobalStateProps } from "./types";

const getAllData = (props: GlobalStateProps) => {
    fetch(`/api/alldata?` + new URLSearchParams({
        pageno: props.globalState.crimeList.page_no.toString(),
        pagesize: props.globalState.crimeList.page_size.toString()
    }))
      .then(response => response.json())
      .then(json => {
        props.setGlobalState({
            ...props.globalState,
            crimeList: {
                ...props.globalState.crimeList,
                data: json["data"]
            }
        })
      })
      .catch(error => console.log(error));
}

export { getAllData }