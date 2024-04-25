import React, { ChangeEvent, useEffect, useRef } from "react";
import { GlobalState, type GlobalStateProps } from "../../types";

import "./FilterSection.css"
import { getAllData } from "../../api-interface";

const FilterSection = (props:GlobalStateProps) => {
    const firstUpdate = useRef(true);

    useEffect(() => {
        if(firstUpdate.current) {
            firstUpdate.current = false
            return;
        }
        getAllData(props)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [props.globalState.crimeList.page_no])

    const longLatChangeHandler = (e:React.ChangeEvent<HTMLInputElement>) => {
        props.setGlobalState((prev:GlobalState) => {
            return { ...prev, filters: {
                ...prev.filters,
                [e.target.name] : e.target.value
            } }
        })
    }

    const onDateChangeHandler = (arg : string, e: ChangeEvent<HTMLInputElement>) => {
        props.setGlobalState((prev) => {
            return { ...prev, filters: {
                    ...prev.filters,
                    [arg]: e.target.value
                }
            }
        })
    }

    const onPageChangeHandler = (e: ChangeEvent<HTMLInputElement>) => {
        props.setGlobalState((prev) => {
            let page = parseInt(e.target.value)
            page = Math.max(1, page)
            return {
                ...prev,
                crimeList: {
                    ...prev.crimeList,
                    page_no: page
                }
            }
        })
    }

    const handlePageChange = (type: string) => {
        if(type === "+") {
            props.setGlobalState((prev) => {
                return {
                    ...prev,
                    crimeList: {
                        ...prev.crimeList,
                        page_no: prev.crimeList.page_no+1
                    }
                }
            })
        }
        if(type === "-") {
            props.setGlobalState((prev) => {
                return {
                    ...prev,
                    crimeList: {
                        ...prev.crimeList,
                        page_no: Math.max(prev.crimeList.page_no-1, 1)
                    }
                }
            })
        }
    }
    
    const handleSubmit = () => {
        props.setGlobalState((prev) => {
            if(prev.crimeList.page_no === 1) {
                getAllData(props)
            }
            return {
                ...prev,
                crimeList: {
                    ...prev.crimeList,
                    page_no: 1
                }
            }
        })
    }

    return (
        <div id="filter-section">
            <div id="filter-fields">
                <span>
                    <input id="latitudebox" onChange={longLatChangeHandler} className="textboxes" type="number" name="lat" value={props.globalState.filters.lat} />
                    <label htmlFor="latitudebox">Latitude</label>
                </span>
                <span>
                    <input id="longitudebox" onChange={longLatChangeHandler} className="textboxes" type="number" name="name" value={props.globalState.filters.long} />
                    <label htmlFor="longitudebox">Longitude</label>
                </span>
                <span id="date1">
                    <input id="startdate" type="date" max={props.globalState.filters.endDate} onChange={onDateChangeHandler.bind(null, "startDate")} value={props.globalState.filters.startDate} />
                    <label htmlFor="startdate">Start date</label>
                </span>
                <span id="date2">
                    <input id="enddate" type="date" min={props.globalState.filters.startDate} max={new Date().toJSON().slice(0, 10)} onChange={onDateChangeHandler.bind(null, "endDate")} value={props.globalState.filters.endDate} />
                    <label htmlFor="enddate">End date</label>
                </span>
            </div>
            <button onClick={handleSubmit}>Search</button>
            <div id="page-fields">
                <button onClick={handlePageChange.bind(null, "-")}>&lt;</button>
                <span>
                    <input id="pageno" onChange={onPageChangeHandler} className="textboxes" type="number" name="page" value={props.globalState.crimeList.page_no} />
                    <label htmlFor="pageno">Page no.</label>
                </span>
                <button onClick={handlePageChange.bind(null, "+")}>&gt;</button>
            </div>
        </div>
    );
}

export default FilterSection;