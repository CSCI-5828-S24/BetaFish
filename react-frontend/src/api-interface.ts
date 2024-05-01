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

const getCrimeFreq = (props: GlobalStateProps) => {
  
    fetch('/api/crime_freq')
    .then(response => response.json())
    .then(json => {
        props.setGlobalState((prev) => {
            return {
                ...prev,
                analytics: {
                    ...prev.analytics,
                    freq: {
                      ...prev.analytics.freq,
                      labels: json["data"].map((x:{DAY:string, COUNT:number}) => x["DAY"]),
                      datasets: [
                          {
                              ...prev.analytics.totals.datasets[0],
                              data: json["data"].map((x:{DAY:string, COUNT:number}) => x["COUNT"])
                          }
                      ]
                    }
                }
            }
        })
    })
    .catch(error => console.log(error));

}

const getCrimeTotals = (props: GlobalStateProps) => {
    fetch('/api/crime_totals')
    .then(response => response.json())
    .then(json => {
      props.setGlobalState((prev) => {
          return {
              ...prev,
              analytics: {
                  ...prev.analytics,
                  totals: {
                    ...prev.analytics.totals,
                    labels: json["data"].map((x:{OFFENSE_CATEGORY_ID:string, COUNT:number}) => x["OFFENSE_CATEGORY_ID"]),
                    datasets: [
                        {
                            ...prev.analytics.totals.datasets[0],
                            data: json["data"].map((x:{OFFENSE_CATEGORY_ID:string, COUNT:number}) => x["COUNT"])
                        }
                    ]
                  }
              }
          }
      })
    })
    .catch(error => console.log(error));
}



export { getAllData, getCrimeFreq, getCrimeTotals }