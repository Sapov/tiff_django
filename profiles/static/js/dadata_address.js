var token = "a4de629c3a72adbf3ba1490745eb4f1c9d3070c5";

var type  = "ADDRESS";
var $region = $("#id_region");
var $city   = $("#id_city");
var $street = $("#id_street");
var $house  = $("#id_house");



// регион и район
$region.suggestions({
  token: token,
  type: type,
  hint: false,
  bounds: "region-area"
});

// город и населенный пункт
$city.suggestions({
  token: token,
  type: type,
  hint: false,
  bounds: "city-settlement",
  constraints: $region
});

// улица
$street.suggestions({
  token: token,
  type: type,
  hint: false,
  bounds: "street",
  constraints: $city,
  count: 15
});

// дом
$house.suggestions({
  token: token,
  type: type,
  hint: false,
  noSuggestionsHint: false,
  bounds: "house",
  constraints: $street
});

console.log($house.suggestions())