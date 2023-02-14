import { mydata } from "./data/ward.js";
console.log(mydata);

var map = L.map("map").setView([19.147, 72.833],11);
map.doubleClickZoom.disable();

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 11,
}).addTo(map);

// L.geoJSON(mydata).addTo(map);

function getColor(d) {
  return d > 7000
    ? "#800026"
    : d > 5000
    ? "#BD0026"
    : d > 2000
    ? "#E31A1C"
    : d > 1000
    ? "#FC4E2A"
    : d > 500
    ? "#FD8D3C"
    : d > 200
    ? "#FEB24C"
    : d > 100
    ? "#FED976"
    : "#FFEDA0";
}

function style(feature) {
  // var fe=feature.properties.waste[sliderInput];
  // typeof(fe);
  return {
    fillColor: getColor(feature.properties.waste[sliderInput]),
    weight: 2,
    opacity: 1,
    color: "white",
    dashArray: "3",
    fillOpacity: 0.7,
  };
}



var wardData=mydata;

var slider = document.getElementById("myRange");
var year = document.getElementById("year");
var month = document.getElementById("month");


// Default to show on map 
function highlightFeature(e) {
  var layer = e.target;

  layer.setStyle({
    weight: 5,
    color: "#666",
    dashArray: "",
    fillOpacity: 0.7,
  });

  layer.bringToFront();
}

function resetHighlight(e) {
  geojson.resetStyle(e.target);
}

function onEachFeature(feature, layer) {
  layer.on({
    mouseover: highlightFeature,
    mouseout: resetHighlight,
    // click: zoomToFeature
  });
}

var geojson = L.geoJSON(wardData, {
  style: style,
  onEachFeature: onEachFeature,
});

geojson.addTo(map);

// end default map view
/// uppper part is static


var output = document.getElementById("demo");
output.innerHTML = slider.value;
var sliderInput;

//  On change slider event 
slider.oninput = function () {
  sliderInput = this.value;

  output.innerHTML = this.value;

  function highlightFeature(e) {
    var layer = e.target;
  
    layer.setStyle({
      weight: 5,
      color: "#666",
      dashArray: "",
      fillOpacity: 0.7,
    });
  
    layer.bringToFront();
  }
  
  function resetHighlight(e) {
    geojson.resetStyle(e.target);
  }
  
  function onEachFeature(feature, layer) {
    layer.on({
      mouseover: highlightFeature,
      mouseout: resetHighlight,
      // click: zoomToFeature
    });
  }
  
  var geojson = L.geoJSON(mydata, {
    style: style,
    onEachFeature: onEachFeature,
  });
  
  geojson.addTo(map);


};


