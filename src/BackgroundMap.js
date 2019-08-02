import React, { Component } from 'react';
import {generatePolylines} from './Polylines.js';
import {GOOGLE_MAPS_ENDPOINT} from './Constants.js';
import {BACKGROUND_MAP_STYLE} from './MapStyle.js';
import {withScriptjs, withGoogleMap, GoogleMap} from 'react-google-maps'

const MOUNTAIN_VIEW_COORDINATES = { lat: 37.3861, lng: -122.0839 };
const DEFAULT_ZOOM = 9;

var polylines = generatePolylines();

const MapComponent = withScriptjs(withGoogleMap((props) =>
  <GoogleMap
    defaultZoom={DEFAULT_ZOOM}
    defaultCenter={MOUNTAIN_VIEW_COORDINATES}
    defaultOptions={{
            // defaultCenter: {lat: -34.397, lng: 150.644 },
            styles: BACKGROUND_MAP_STYLE,
            disableDefaultUI: true,
            mapTypeId: 'roadmap',//google.maps.MapTypeId.TERRAIN,
          }}
  >
  {polylines}
  </GoogleMap>
))

//include loading animation when no prompt is loading.
class BackgroundMap extends Component {

  render() {
    return <MapComponent
    isMarkerShown
    googleMapURL={GOOGLE_MAPS_ENDPOINT}
    loadingElement={<div style={{ height: `100%` }} />}
    containerElement={<div style={{ height: `100%` }} />}
    mapElement={<div style={{ height: `100%` }} />}
    />
  }
}


export default BackgroundMap;
