import React from "react";

import "./Header.css"

const Header = () => {
    return (
        <div id="header">
            <h1>Betafish Crime Spotter</h1>
            <div id="navbar">
                <input id="navsearch" type="radio" name="nav" value="search" hidden/>
                <label className="navbutton" htmlFor="navsearch">Search</label>
                <input id="navanalytics" type="radio" name="nav" value="analytics" hidden/>
                <label className="navbutton" htmlFor="navanalytics">Analytics</label>
            </div>
        </div>
    );
}

export default Header;