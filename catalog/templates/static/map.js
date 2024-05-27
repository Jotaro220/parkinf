DG.then(function () {
  var map,
      myIcon,

  map = DG.map('map', {
      center: [55.983787, 37.217787],
      zoom: 16,
    minZoom: 11,
    maxZoom: 20
  });

  myIcon = DG.icon({
      iconUrl: 'pictures/icon.svg',
      iconSize: [50, 50]
          // iconUrl:"https://static.2gis.com/files/d678c972e068d887.png"
      // iconSize: [25, 25]
  });
  DG.marker([55.983787, 37.217787], {
      icon: myIcon
  }).addTo(map).bindLabel('ParkINF',{static: true});

});