// noinspection JSDeprecatedSymbols
// const locations = [{position: { lat: 38.0356, lng: -78.5034 }, primary_key: 1}, {position: { lat: 38.0366, lng: -78.5034 }, primary_key: 2}];
function getUrl(url = "/"){
  if(!url.startsWith("/")){
    url = "/" + url;
  }
  return "http://"+window.location.host+url;
}

function fetchResource(url){
   return fetch(getUrl(url), {
        headers: {
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest',
        },
      })
}

function createAddStudySpace() {
  const addStudySpaceButton = document.createElement("button");
  addStudySpaceButton.style.height = "40px";
  addStudySpaceButton.style.width = "40px";
  addStudySpaceButton.style.backgroundColor = "#fff";
  addStudySpaceButton.style.border = "2px solid #fff";
  addStudySpaceButton.style.margin = "10px";
  addStudySpaceButton.style.padding = "0px";
  addStudySpaceButton.style.borderRadius = "2px";
  addStudySpaceButton.style.boxShadow = "0px 1px 4px -1px rgba(0,0,0,.3)";
  addStudySpaceButton.style.cursor = "pointer";
  addStudySpaceButton.style.lineHeight = "38px";
  addStudySpaceButton.style.overflow = "hidden";
  addStudySpaceButton.style.textAlign = "center";
  addStudySpaceButton.title = "Click to add a study spot";
  addStudySpaceButton.type = "button";
  addStudySpaceButton.addEventListener("click", () => {
    window.location.href = getUrl('add');
  });
  const addStudySpaceIcon = document.createElement('img');
  addStudySpaceIcon.src = icon;
  addStudySpaceIcon.style.height = "24px";
  addStudySpaceIcon.style.width = "24px";
  addStudySpaceIcon.style.filter = "invert(47%) sepia(0%) saturate(252%) hue-rotate(202deg) brightness(81%) contrast(85%)"; //#666666
  addStudySpaceButton.appendChild(addStudySpaceIcon);
    addStudySpaceButton.addEventListener("mouseleave", (event) => {
      addStudySpaceIcon.style.filter = "invert(47%) sepia(0%) saturate(252%) hue-rotate(202deg) brightness(81%) contrast(85%)"; //#666666
  });
  addStudySpaceButton.addEventListener("mouseenter", (event) => {
      addStudySpaceIcon.style.filter = "invert(20%) sepia(0%) saturate(0%) hue-rotate(188deg) brightness(89%) contrast(95%)"; //#333333
  });
  return addStudySpaceButton;
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
  const addStudySpaceButton = createAddStudySpace(); //creates
  centerControlDiv.appendChild(addStudySpaceButton);
  map.controls[google.maps.ControlPosition.RIGHT_CENTER].push(addStudySpaceButton);
  var infowindow = new google.maps.InfoWindow({
     content: ""
   });
  locations.forEach((location, i) => {
    const pin = new google.maps.marker.PinElement({
    })
    const marker = new google.maps.marker.AdvancedMarkerElement({
      position: location.coordinates,
      map,
      title: location.name,
      zIndex: location.location_id,
      content: pin.element,
    });
    marker.addListener("click", ({ domEvent, latLng }) => {
      const { target } = domEvent;
      infowindow.close();
      infowindow.setContent(makeWindowContent(location));
      fetchResource(get_location_data_url(location.location_id))
      .then((response) => response.json())
      .then((data) =>{
      infowindow.setContent(makeWindowContent(location, data))
      }).then(infowindow.open(map, marker));
    });
    if(starting_location_id && starting_location_id === location.location_id){
        new google.maps.event.trigger(marker, "click");
        infowindow.focus();
    }
  })

}

function makeWindowContent(location, data= null){
  return '<h3> ' + location.name + '</h3>' +
         '<h6>' + location.location_type + '</h6>' +
         '<p>' + location.address + '</p>' + (data == null ? "" : formatPostLinks(location, data))
}

function formatPostLinks(location, data){
  let output = "";
  data.forEach(function(studyspace){
    output += `<a href="${getUrl(get_studyspace_data_url(location.location_id, studyspace.location_ordinal))}"`+
              `title="${studyspace.space_type}: (fix ratings out of 5)">${studyspace.name}</a><br>`;
  });
  output += '<a href="'+getUrl(get_add_with_location_url(location.location_id))+'">Add a new study spot</a>'
  return output;
}

//   function placeMarkerAndPanTo(latLng, map) {
//     new PinElement({
//     position: latLng,
//     map: map,
//   });
//   map.panTo(latLng);
// }

window.initMap = initMap;