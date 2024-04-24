import React, { ChangeEvent } from "react";
import { GlobalState, type GlobalStateProps } from "../../types";

import "./FilterSection.css"
import { getAllData } from "../../api-interface";

const FilterSection = (props:GlobalStateProps) => {
    const handleChange = (e:React.ChangeEvent<HTMLInputElement>) => {
        props.setGlobalState((prev:GlobalState) => {
            return { ...prev, filters: {
                ...prev.filters,
                [e.target.name] : e.target.value
            } }
        })
    }

    const onDateChange = (arg : string, e: ChangeEvent<HTMLInputElement>) => {
        props.setGlobalState((prev) => {
            return { ...prev, filters: {
                    ...prev.filters,
                    [arg]: e.target.value
                }
            }
        })
    }
    
    const handleDump = () => {
      getAllData(props)
    }
    console.log(props.globalState.crimeList)

    return (
        <div id="filter-section">
            <input onChange={handleChange} className="textboxes" type="number" name="name" value={props.globalState.filters.long? "":props.globalState.filters.long as number} />
            <input className="textboxes" type="number" name="lat" value={props.globalState.filters.lat? "":props.globalState.filters.lat as number} />
            <input type="date" onChange={onDateChange.bind(null, "startDate")} value={props.globalState.filters.startDate} />
            <input type="date" onChange={onDateChange.bind(null, "endDate")} value={props.globalState.filters.endDate} />
            <button onClick={handleDump}>Database Dump</button>
        </div>
    );
}

export default FilterSection;