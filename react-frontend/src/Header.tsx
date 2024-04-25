import React, { ChangeEvent } from "react";

import "./Header.css"
import { GlobalStateProps } from "./types";

const Header = (props: GlobalStateProps) => {
    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        props.setGlobalState(prev => {
            return {
                ...prev,
                active: e.target.value
            }
        })
    }

    return (
        <div id="header">
            <h1>Betafish Crime Spotter</h1>
            <div id="navbar">
                <input onChange={handleChange} id="navsearch" type="radio" name="nav" value="search" hidden checked={props.globalState.active === "search"}/>
                <label className="navbutton" htmlFor="navsearch">Search</label>
                <input onChange={handleChange} id="navanalytics" type="radio" name="nav" value="analytics" hidden checked={props.globalState.active === "analytics"}/>
                <label className="navbutton" htmlFor="navanalytics">Analytics</label>
            </div>
        </div>
    );
}

export default Header;