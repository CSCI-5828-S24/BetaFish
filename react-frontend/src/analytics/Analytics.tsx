import { GlobalStateProps } from "../types";

const Analytics = (props: GlobalStateProps) => {
    return (
        <div id="analytics-div" className={props.globalState.active === "analytics"? "sectionactive":""}>
            <p>Something</p>
        </div>
    );
}

export default Analytics;