import React from "react";

type DateValuePiece = Date | null;

type DateValue = DateValuePiece | [DateValuePiece, DateValuePiece]

type GlobalState = {
    filters: {
        long: number | null;
        lat: number | null;
        startDate: DateValue | null;
        endDate: DateValue | null;
    };
    crimeList: [];
}

type GlobalStateProps = {
    globalState: GlobalState;
    setGlobalState: React.Dispatch<React.SetStateAction<GlobalState>>;
}

export type { GlobalState, GlobalStateProps, DateValue }