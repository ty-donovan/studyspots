// noinspection JSDeprecatedSymbols

let map

function initMap(){
    const originalMapCenter = new google.maps.LatLng(38.0356, -78.5034);
    map = new google.maps.Map(document.getElementById("map"),{
        mapId: "86be248947f98a57",
        center:originalMapCenter,
        zoom: 17,
    });
  const infowindow = new google.maps.InfoWindow({
    content: "Change the zoom level",
    position: originalMapCenter,
  });

  infowindow.open(map);
  map.addListener("zoom_changed", () => {
    infowindow.setContent("Zoom: " + map.getZoom());
  });
    //addListener is google api specific
    map.addListener("click", (e) => {
        placeMarkerAndPanTo(e.latLng, map);
    });
}

function placeMarkerAndPanTo(latLng, map) {
    new google.maps.Marker({
    position: latLng,
    map: map,
  });
  map.panTo(latLng);
}

window.initMap = initMap