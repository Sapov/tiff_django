var token = "a4de629c3a72adbf3ba1490745eb4f1c9d3070c5";

$("#bank").change(function(e) {
  var promise = suggest(e.target.value);
  promise
  	.done(function(response) {
      showBank(response.suggestions)
      console.log(response);
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
      console.log(textStatus);
      console.log(errorThrown);
    });
});

function suggest(query) {
  var serviceUrl = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/bank";
  var request = {
    "query": query
  };
  var params = {
    type: "POST",
    contentType: "application/json",
    headers: {
      "Authorization": "Token " + token
    },
    data: JSON.stringify(request)
  }
  
	return $.ajax(serviceUrl, params);
}

function clearBank() {
  $("#id_bank_name").val("");
//  $("#id_bank_name").val("");
  $("#id_bik_bank").val("");
  $("#id_bankCorrAccount").val("");
  $("#id_address_post").val("");
}

function showBank(suggestions) {
  clearBank();
  if (suggestions.length === 0) return;
  var bank = suggestions[0].data;
  $("#id_bank_name").val(bank.name && bank.name.payment || "");
  $("#name_full").val(bank.name && bank.name.full || "");
  $("#id_bik_bank").val(bank.bic);
  $("#id_bankCorrAccount").val(bank.correspondent_account);
  $("#id_address_post").val(bank.address.value);

}