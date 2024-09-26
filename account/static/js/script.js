//require('dotenv').config();

//var token = process.env.TOKEN_DADATA;
var token ='a4de629c3a72adbf3ba1490745eb4f1c9d3070c5';


function join(arr /*, separator */) {
  var separator = arguments.length > 1 ? arguments[1] : ", ";
  return arr.filter(function(n){return n}).join(separator);
}

function typeDescription(type) {
  var TYPES = {
    'INDIVIDUAL': 'Индивидуальный предприниматель',
    'LEGAL': 'Организация'
  }
  return TYPES[type];
}

function showSuggestion(suggestion) {
  console.log(suggestion);
  var data = suggestion.data;
  if (!data)
    return;
  
  $("#type").text(
    typeDescription(data.type) + " (" + data.type + ")"
  );

  if (data.name)
    $("#name_short").val(join([data.opf && data.opf.short || "", data.name.short || data.name.full], " "));
  
  if (data.name && data.name.full)
    $("#id_name_full").val(join([data.opf && data.opf.full || "", data.name.full], " "));
  
  $("#id_inn").val(data.inn);

  $("#id_kpp").val(data.kpp);

  if (data.address)
    $("#id_address").val(data.address.value);
}

$("#party").suggestions({
  token: token,
  type: "PARTY",
  count: 5,
  params: {
    branch_type: ["MAIN"],
  },
  onSelect: showSuggestion
});