// Update select boxes
var nameSelect = document.getElementById("corp_name"); 
for(var i = 0; i < names.length; i++) {
  
    // Update name select box
    var option = document.createElement("option");
    option.textContent = names[i];
    option.value = names[i];
    nameSelect.appendChild(option);
}

// Update ticker select box
var tickerSelect = document.getElementById("tickers"); 
for(var i = 0; i < tickers.length; i++) {
  
    option = document.createElement("option");
    option.textContent = tickers[i];
    option.value = tickers[i];
    tickerSelect.appendChild(option);
}

function displayOutput(status, response, ticker) {
  
  // Show panel
  var panel = document.getElementById("panel");
  panel.style.visibility = 'visible';
  
  if(status === null) {
    panel.innerHTML = "The current price of ".concat(response['companyName']).concat(' is <b>$').concat(response['latestPrice']).concat('</b>. Plutocracy predicts that today\'s high will be <b>$XXX.XX</b> and the low will be <b>$YYY.YY</b>.');
  } else {
    panel.innerHTML = "Could not access stock information for ".concat(ticker).concat(": ").concat(status);
  }
}

function getJSON(url, ticker) {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);
  xhr.responseType = 'json';
  xhr.onload = function() {
    var status = xhr.status;
    if (status === 200) {
      displayOutput(null, xhr.response, ticker);
    } else {
      displayOutput(status, xhr.response, ticker);
    }
  };
  xhr.send();
};

function nameChange(name) {
  var startPos = name.indexOf("(");
  var endPos = name.indexOf(")");
  var ticker = name.substring(startPos+1, endPos).toLowerCase();
  url = "https://api.iextrading.com/1.0/stock/".concat(ticker).concat("/quote");
  getJSON(url, ticker);
}

function tickerChange(name) {
  var pos = name.indexOf(" (");
  var ticker = name.substring(0, pos).toLowerCase();
  url = "https://api.iextrading.com/1.0/stock/".concat(ticker).concat("/quote");
  getJSON(url, ticker);
}

