import React, { useState, useRef, useEffect, useCallback } from 'react'
import mapboxgl from "mapbox-gl/dist/mapbox-gl";
import { useStore } from "./store";
import Navigation from './components/navigation';
import MapView from './views/map';
import { Link, Route, useRoute } from "wouter";

import 'mapbox-gl/dist/mapbox-gl.css';
import View from './components/view';
import BuildingsList from './views/buildings/list';
import AmenitiesList from './views/amenities/list';
import AmenitiesSingle from './views/amenities/single';
import BuildingsSingle from './views/buildings/single';
import LoginView from './views/login';
import FloorsSingle from './views/floors/single';

mapboxgl.accessToken = "pk.eyJ1IjoiMmNvbm5lY3QiLCJhIjoiY2xmYnliN3hrMzVleDNvcjBrejFlMHppdCJ9.SAgfhr7EcoC5LJPsWXm-mA"

const App = () => {

  const apiToken = useStore(state => state.apiToken);

  if (apiToken === null) {
    return <LoginView />
  }

  return <React.Fragment>
    <Navigation />
    <View>
      <Route path="/buildings"><BuildingsList /></Route>
      <Route path="/buildings/:id">{({ id }) => <BuildingsSingle id={id} />}</Route>
      <Route path="/buildings/:bid/floors/:id">{({ id }) => <FloorsSingle id={id} />}</Route>
      <Route path="/amenities"><AmenitiesList /></Route>
      <Route path="/amenities/:id">{({ id }) => <AmenitiesSingle id={id} />}</Route>
    </View>
  </React.Fragment>

}

export default App
