function confirmButtonClick() {
  var time = '4M2';
  searchFreeRooms({time: time}, function(result) {
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
