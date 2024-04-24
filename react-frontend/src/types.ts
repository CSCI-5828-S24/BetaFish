import React from "react";

type GlobalState = {
    filters: {
        long: number;
        lat: number;
        startDate: string;
        endDate: string;
    };
    fetched: boolean;
    crimeList: {
        page_no: number;
        page_size: number;
        data: any[]
    };
}

type GlobalStateProps = {
    globalState: GlobalState;
    setGlobalState: React.Dispatch<React.SetStateAction<GlobalState>>;
}

export type { GlobalState, GlobalStateProps }