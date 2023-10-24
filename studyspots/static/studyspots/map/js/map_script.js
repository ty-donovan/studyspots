// noinspection JSDeprecatedSymbols
const locations = [{position: { lat: 38.0356, lng: -78.5034 }, primary_key: 1}, {position: { lat: 38.0456, lng: -78.5034 }, primary_key: 2}];
function createAddSpotButton() {
  const addSpotButton = document.createElement("button");
  addSpotButton.style.height = "40px";
  addSpotButton.style.width = "40px";
  addSpotButton.style.backgroundColor = "#fff";
  addSpotButton.style.border = "2px solid #fff";
  addSpotButton.style.margin = "10px";
  addSpotButton.style.padding = "0px";
  addSpotButton.style.borderRadius = "2px";
  addSpotButton.style.boxShadow = "0px 1px 4px -1px rgba(0,0,0,.3)";
  addSpotButton.style.cursor = "pointer";
  addSpotButton.style.lineHeight = "38px";
  addSpotButton.style.overflow = "hidden";
  addSpotButton.style.textAlign = "center";
  addSpotButton.title = "Click to add a study spot";
  addSpotButton.type = "button";
  addSpotButton.addEventListener("click", () => {
    console.log("yup")
  });
  const addSpotIcon = document.createElement('img');
  addSpotIcon.src = icon;
  addSpotIcon.style.height = "24px";
  addSpotIcon.style.width = "24px";
  addSpotIcon.style.filter = "invert(47%) sepia(0%) saturate(252%) hue-rotate(202deg) brightness(81%) contrast(85%)"; //#666666
  addSpotButton.appendChild(addSpotIcon);
    addSpotButton.addEventListener("mouseleave", (event) => {
      addSpotIcon.style.filter = "invert(47%) sepia(0%) saturate(252%) hue-rotate(202deg) brightness(81%) contrast(85%)"; //#666666
  });
  addSpotButton.addEventListener("mouseenter", (event) => {
      addSpotIcon.style.filter = "invert(20%) sepia(0%) saturate(0%) hue-rotate(188deg) brightness(89%) contrast(95%)"; //#333333
  });
  return addSpotButton;
}

// Initialize and add the map
let map;

function initMap() {
  const startingPosition = { lat: 38.0356, lng: -78.5034 };
  map = new google.maps.Map(document.getElementById("map"), {
        mapId: "86be248947f98a57",
        center: startingPosition,
        zoom: 17,
        mapTypeControl: false,
        streetViewControl: false,
  });
  const centerControlDiv = document.createElement("div");
  const addSpotButton = createAddSpotButton(); //creates
  centerControlDiv.appendChild(addSpotButton);
  map.controls[google.maps.ControlPosition.RIGHT_CENTER].push(addSpotButton);
  var infowindow = new google.maps.InfoWindow({
     content: "Blank infowindow"
   });
  locations.forEach(({position, primary_key}, i) => {
    const pin = new google.maps.marker.PinElement({
    })
    const marker = new google.maps.marker.AdvancedMarkerElement({
      position,
      map,
      title: `${primary_key}`,
      content: pin.element,
    });
    marker.addListener("click", ({ domEvent, latLng }) => {
      const { target } = domEvent;
      infowindow.setContent('<div>' +
                '<h3> key_' + marker.title + '</h3>' +
                '<p> word  </p>' +
                '<a href="'+marker.title+'">Location Page</a>' +
                '</div>');
      infowindow.open(map, marker)
      console.log(marker.title)
    });
  })
}

//   function placeMarkerAndPanTo(latLng, map) {
//     new PinElement({
//     position: latLng,
//     map: map,
//   });
//   map.panTo(latLng);
// }

window.initMap = initMap;