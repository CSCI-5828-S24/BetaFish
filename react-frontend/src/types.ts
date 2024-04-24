import React from "react";

type GlobalState = {
    filters: {
        long: number | null;
        lat: number | null;
        startDate: string;
        endDate: string;
    };
    crimeList: {
        page_no: number;
        page_size: number;
        data: []
    };
}

type GlobalStateProps = {
    globalState: GlobalState;
    setGlobalState: React.Dispatch<React.SetStateAction<GlobalState>>;
}

export type { GlobalState, GlobalStateProps }