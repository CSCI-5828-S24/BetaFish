import React from "react";
import MapSection from "./map-section/MapSection";
import FilterSection from "./filter-section/FilterSection";
import { GlobalStateProps } from "../types";

import "./Search.css"

const Search = (props:GlobalStateProps) => {
    return (
        <div id="search-div">
            <MapSection />
            <FilterSection globalState={props.globalState} setGlobalState={props.setGlobalState}/>
        </div>
    );
}

export default Search;