import React from 'react';
import {EXAMPLE_TRIP_DATA} from './Constants.js';
import {lineSymbol, Polyline} from 'react-google-maps'

function generatePolyline(lat,lng,prev_lat,prev_lng, color_hex){
  var pathCoordinates = [
        { lat: prev_lat, lng: prev_lng },
        { lat: lat, lng: lng }
    ];
  var lat_string = lat.toString();
  var lng_string = lng.toString();
  return <Polyline
      key={`${lat_string}-${lng_string}`}
      path={pathCoordinates}
      geodesic={true}
      options={{
          strokeColor: color_hex,
          strokeOpacity: 0.75,
          strokeWeight: 7,
          lineJoin:"round"
      }}
  />
}

export function generatePolylines(){
  var polylines = [];
  console.log(EXAMPLE_TRIP_DATA.length)
  for (var i = 1; i < EXAMPLE_TRIP_DATA.length; i++) {
    var trip = EXAMPLE_TRIP_DATA[i]
    console.log(trip)
    var polyline = generatePolyline(trip.lat,trip.lng,trip.prev_lat,trip.prev_lng, trip.color);
    polylines = polylines.concat(polyline);
  }
  console.log(polylines)
  return polylines;
}
