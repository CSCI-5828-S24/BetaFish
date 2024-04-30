import { GlobalStateProps } from "./types";

const getAllData = (props: GlobalStateProps) => {
    fetch(`/api/alldata?` + new URLSearchParams({
        startTime: new Date(props.globalState.filters.startDate).getTime().toString(),
        endTime: new Date(props.globalState.filters.endDate).getTime().toString(),
        lat: props.globalState.filters.lat.toString(),
        long: props.globalState.filters.long.toString(),
        pageno: props.globalState.crimeList.page_no.toString(),
        pagesize: props.globalState.crimeList.page_size.toString(),
    }))
      .then(response => response.json())
      .then(json => {
        props.setGlobalState((prev) => {
            return {
                ...prev,
                crimeList: {
                    ...prev.crimeList,
                    data: json["data"]
                }
            }
        })
      })
      .catch(error => console.log(error));
}

const getCrimeCounts = (props: GlobalStateProps) => {
    fetch ("/api/crime_totals")
        .then(response => response.json())
        .then(json => {
            props.setGlobalState((prev) => {
                return {
                    ...prev, 
                    crimeTotals: {
                        ...prev.crimeTotals,
                        data: json["data"]
                    }
                }
            })
        })
        .catch(error => console.log(error))
}

export { getAllData, getCrimeCounts }