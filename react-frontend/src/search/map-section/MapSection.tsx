import React from "react";
import { MapContainer, Marker, Popup, TileLayer, useMapEvents } from "react-leaflet";

import "leaflet/dist/leaflet.css"
import "./MapSection.css"
import { GlobalStateProps } from "../../types";

const MapSection = (props: GlobalStateProps) => {
    const HandleMapClick = () => {
        const map = useMapEvents({
            click: (e) => {
                props.setGlobalState((prev)=> {
                    return {
                        ...prev,
                        filters: {
                            ...prev.filters,
                            lat: e.latlng.lat,
                            long: e.latlng.lng
                        }
                    };
                })
            },
        });
        return <></>;
    }

    return (
        <div id="map-section">
            <MapContainer center={[props.globalState.filters.lat, props.globalState.filters.long]} zoom={16} scrollWheelZoom={true}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <HandleMapClick />
                <Marker position={[51.505, -0.09]}>
                    <Popup>
                    A pretty CSS3 popup. <br /> Easily customizable.
                    </Popup>
                </Marker>
            </MapContainer>
        </div>
    );
}

export default MapSection;