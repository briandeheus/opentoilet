import React, { useState, useRef, useEffect, useCallback } from 'react'
import mapboxgl from "mapbox-gl/dist/mapbox-gl";
import styled from 'styled-components';
import { useStore } from "../store";
import { ToiletIcon } from '../components/icons.jsx';
import 'mapbox-gl/dist/mapbox-gl.css';
import Navigation from '../components/navigation';
import BuildingForm from '../components/forms/building';

mapboxgl.accessToken = "pk.eyJ1IjoiMmNvbm5lY3QiLCJhIjoiY2xmYnliN3hrMzVleDNvcjBrejFlMHppdCJ9.SAgfhr7EcoC5LJPsWXm-mA"
const Map = styled.div`
  height: 100%;
  width: 100%;
`

const Button = ({ onClick, children }) => {
    return (
        <button
            onClick={onClick}
            type="button"
            className="rounded-md bg-indigo-600 py-1.5 px-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
        >
            {children}
        </button>
    )
}


const Modal = ({ children, visible = false }) => {
    return <div className={`modal ${visible ? "modal-open" : ""}`}>
        <div className="modal-box">
            {children}
        </div>
    </div>
}

const MapView = () => {

    const [
        apiToken,
        buildings,
        updateBuilding,
        loadBuildings,
    ] = useStore(state => [
        state.apiToken,
        state.buildings,
        state.updateBuilding,
        state.loadBuildings
    ]);

    const [showBuildingModal, setShowBuildingModal] = useState(false);
    const [mapLoaded, setMapLoaded] = useState(false);

    const map = useRef(null);
    const mapContainer = useRef(null);

    useEffect(() => {

        if (mapContainer.current === null) {
            return;
        }

        if (map.current !== null) {
            return;
        }

        map.current = new mapboxgl.Map({
            container: mapContainer.current,
            style: "mapbox://styles/2connect/clfbzcutz002801p7uoe4a4fv",
            zoom: 18,
            center: [139.63076, 35.6199370],
            antialias: true
        });

        map.current.on("click", (event) => {

            const { lngLat } = event;
            console.log("Map click");
            console.log(event);
            //setShowBuildingModal(true);
            updateBuilding("latlng", [lngLat.lat, lngLat.lng]);
            updateBuilding("name", "");

            const selectedFeatures = map.current.queryRenderedFeatures(event.point, {
                layers: ['buildings']
            });

        });

        map.current.on("load", () => {
            setMapLoaded(true);
        });

        let img = new Image(30, 40)
        img.onload = () => {
            map.current.addImage('toilet-icon', img);
        }
        img.src = TOILET_ICON

    }, [mapContainer, mapLoaded]);

    useEffect(() => {

        if (map.current === null) {
            return;
        }

        if (mapLoaded === false) {
            return;
        }

        map.current.addLayer({
            id: `buildings`,
            type: 'symbol',
            source: {
                type: 'geojson',
                data: {
                    type: 'FeatureCollection',
                    features: buildings.map((building) => {
                        return {
                            type: 'Feature',
                            geometry: {
                                type: 'Point',
                                coordinates: [building.latlng[1], building.latlng[0]]
                            },
                            properties: building
                        }
                    })
                }
            },
            layout: {
                'icon-image': 'toilet-icon',
                'text-field': ['get', 'name'],
                'text-font': ['Open Sans Semibold', 'Arial Unicode MS Bold'],
                'text-offset': [0, 1.5],
                'text-anchor': 'top'
            }
        });

    }, [mapLoaded, buildings]);

    useEffect(() => loadBuildings, [apiToken]);

    return <main className="">
        <div className="h-full" ref={mapContainer}></div>
        <Modal visible={showBuildingModal}>
            <BuildingForm />
        </Modal>
    </main>

}

export default MapView
