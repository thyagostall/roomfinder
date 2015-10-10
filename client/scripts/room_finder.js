var BASE_URL = "http://localhost:8000/api/"

function getCourses(callback) {
  $.get(BASE_URL + "importdata/", callback);
}

function saveData(data) {
  $.post(BASE_URL + "importdata/", JSON.stringify(data));
}

function searchFreeRooms(data, success) {
  $.get(BASE_URL + "freeroomat/" + data.time, success);
}

function parseSchedule(data) {
  schedules = data.match(/[0-9][A-Z][0-9]\((\w+[\-]\w+)\)/g);

  for (var i = 0; schedules && i < schedules.length; i++) {
    var temp = schedules[i].split('(');
    schedules[i] = {time: temp[0], room: temp[1].replace(")", "")};
  }

  return schedules;
}

function parseProfessors(data) {
  var result = [];
  var data = data.split('\n');

  for (var i = 0; i < data.length; i++) {
    data[i] = $.trim(data[i]);

    if (data[i] != "")
      result.push(data[i])
  }

  return result;
}

function fillInData(data) {
  var courseName, courseCode = "";
  var courses = [];

  for (var i = 0; i < lines.length; i++) {
    var header = $(lines[i]).find('td.curso')
    if (header.length > 0) {
      if (courseCode != "") {
        courses.push({courseCode, courseName, courseSessions});
      }

      var courseSessions = []
      header = $.trim(header[0].innerText).split(' - ');
      courseCode = header[0];
      courseName = $.trim(header[1].split(' (')[0]);

      i++;
    } else {
      if (lines[i].innerText.search(/turma/i) < 0) {
        fields = $(lines[i]).find('td');
        schedules = parseSchedule($.trim(fields[5].innerText));
        professors = parseProfessors($.trim(fields[6].innerText));

        courseSession = {
          session: $.trim(fields[0].innerText),
          schedule: schedules,
          professor: professors
        };
        courseSessions.push(courseSession);
      }
    }
  }

  if (courses.length > 0) {
    saveData(courses);
  }
}
