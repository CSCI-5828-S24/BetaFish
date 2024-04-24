import React from "react";
import MapSection from "./map-section/MapSection";
import FilterSection from "./filter-section/FilterSection";
import { GlobalStateProps } from "../types";

import "./Search.css"
import CrimeListSection from "./list-section/CrimeListSection";

const Search = (props:GlobalStateProps) => {
    return (
        <div id="search-div">
            <MapSection globalState={props.globalState} setGlobalState={props.setGlobalState}/>
            <FilterSection globalState={props.globalState} setGlobalState={props.setGlobalState}/>
            <CrimeListSection globalState={props.globalState} setGlobalState={props.setGlobalState}/>
        </div>
    );
}

export default Search;