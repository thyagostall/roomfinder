function confirmButtonClick() {
  var time = $("#day")[0].value + $("#class")[0].value;
  var current = $("#result")[0].innerText.split(",");

  current = JSON.stringify(current);
  console.log(current);

  searchFreeRooms({time: time, currentRooms: current}, function(result) {
    $("#result")[0].innerText = result;
  });
}

function importButtonClick() {
  getCourses(function(result) {
    lines = $('tr', result);
    fillInData(lines);
    $("#result").innerText = "Data transfered successfully";
  });
}

function clearButtonClick() {
  $("#result")[0].innerText = "";
}
