import React from "react";
import { MapContainer, Marker, Popup, TileLayer, useMap, useMapEvents } from "react-leaflet";
import dropIconImg from "../../assets/location-pin.png"
import crimeIconImg from "../../assets/crime-pin.png"

import "leaflet/dist/leaflet.css"
import "./MapSection.css"
import { GlobalStateProps } from "../../types";
import { Icon, featureGroup, latLng, marker } from "leaflet";

const MapSection = (props: GlobalStateProps) => {

    const crimeIcon = new Icon({
        iconUrl: crimeIconImg,
        iconSize: [64, 64],
        className: "crimeIcon"
    })

    const dropIcon = new Icon({
        iconUrl: dropIconImg,
        iconSize: [64, 64],
        className: "dropIcon"
    })

    const HandleMapClick = () => {
        useMapEvents({
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
        return null;
    }

    const RecenterMap = () => {
        const map = useMap();
        
            if(props.globalState.crimeList.data.length > 0 && props.globalState.fetched) {
                let group = featureGroup(
                    [
                        marker(
                            latLng(
                                props.globalState.filters.lat,
                                props.globalState.filters.long
                            )
                        ),
                        ...props.globalState.crimeList.data.map((item) => {
                            return marker(
                                latLng(
                                    parseFloat(item["GEO_LAT"]),
                                    parseFloat(item["GEO_LON"])
                                )
                            )
                        })
                    ]
                )
                console.log("centering")
                // map.setView([parseFloat(data[0]["GEO_LAT"]), parseFloat(data[0]["GEO_LON"])]);
                map.fitBounds(group.getBounds(), {
                    animate: true,
                    padding: [10,10]
                })
                props.setGlobalState(prev => {
                    return {
                        ...prev,
                        fetched: false
                    }
                })
                
            }
        
        return null;
    }

    return (
        <div id="map-section">
            <MapContainer center={[props.globalState.filters.lat, props.globalState.filters.long]} zoom={16} scrollWheelZoom={true}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <HandleMapClick />
                <RecenterMap />
                <Marker position={[props.globalState.filters.lat, props.globalState.filters.long]} icon={dropIcon} />
                {
                    props.globalState.crimeList.data.map((item) => {
                        return <Marker position={[parseFloat(item["GEO_LAT"]), parseFloat(item["GEO_LON"])]} icon={crimeIcon}>
                            <Popup>
                                <p>{item["OFFENSE_TYPE_ID"]}</p>
                            </Popup>
                        </Marker>
                    })
                }
            </MapContainer>
        </div>
    );
}

export default MapSection;