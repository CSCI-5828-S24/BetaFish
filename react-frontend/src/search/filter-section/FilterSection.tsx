import React from "react";
import { DateValue, GlobalState, type GlobalStateProps } from "../../types";
import DatePicker from "react-date-picker";

import 'react-date-picker/dist/DatePicker.css';
import 'react-calendar/dist/Calendar.css';

const FilterSection = (props:GlobalStateProps) => {
    const handleChange = (e:React.ChangeEvent<HTMLInputElement>) => {
        props.setGlobalState((prev:GlobalState) => {
            return { ...prev, filters: {
                ...prev.filters,
                [e.target.name] : e.target.value
            } }
        })
    }

    const onDateChange = (arg : string, value: DateValue) => {
        props.setGlobalState((prev) => {
            return { ...prev, filters: {
                    ...prev.filters,
                    [arg]: value
                }
            }
        })
    }

    return (
        <div>
            <input onChange={handleChange} className="textboxes" type="number" name="name" value={props.globalState.filters.long? "":props.globalState.filters.long as number} />
            <input className="textboxes" type="number" name="lat" value={props.globalState.filters.lat? "":props.globalState.filters.lat as number} />
            <DatePicker onChange={onDateChange.bind(null, "startDate")} value={props.globalState.filters.startDate} />
            <DatePicker onChange={onDateChange.bind(null, "endDate")} value={props.globalState.filters.endDate} />
        </div>
    );
}

export default FilterSection;