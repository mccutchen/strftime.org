
var dateEntry = document.getElementById('date-entry');
var output = document.getElementById('date-output');

dateEntry.onkeyup = function(e) {
  var strf = dateEntry.value;
  var date = null;
  if (strf.endsWith('%')) {
    date = 'ValueError: strftime format ends with raw %';
  } else {
    date = strftime(strf);
  }

  output.textContent = date;
};
