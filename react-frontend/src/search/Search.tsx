import React from "react";
import MapSection from "./map-section/MapSection";
import FilterSection from "./filter-section/FilterSection";
import { GlobalStateProps } from "../types";

const Search = (props:GlobalStateProps) => {
    return (
        <div>
            <MapSection />
            <FilterSection globalState={props.globalState} setGlobalState={props.setGlobalState}/>
        </div>
    );
}

export default Search;