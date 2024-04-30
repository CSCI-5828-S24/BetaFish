import React from "react";

type GlobalState = {
    active: string;
    filters: {
        long: number;
        lat: number;
        startDate: string;
        endDate: string;
    };
    map: {
        lat: number;
        long: number;
    };
    crimeList: {
        page_no: number;
        page_size: number;
        data: any[]
    };
    crimeTotals: {
        data: any[]
    }
}

type GlobalStateProps = {
    globalState: GlobalState;
    setGlobalState: React.Dispatch<React.SetStateAction<GlobalState>>;
}

export type { GlobalState, GlobalStateProps }