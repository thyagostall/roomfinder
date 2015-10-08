// Algorithm
//
// Find all course codes
// For all courses download the page of open classes
// For all classes of that course, parse the table and find classes, room, schedule relation
//
// [0-9][A-Z][0-9]\((\w*[\-]\w*)\)

function findMajors() {

}

function getCourses(callback) {
  $.get("http://localhost:8000/api/getdata/", callback);
}

function saveCourse(data) {
  console.log(data);
}

function parseSchedule(data) {
  return data.match(/[0-9][A-Z][0-9]\((\w*[\-]\w*)\)/g);
}

function parseProfessors(data) {
  var result = [];
  var data = data.split('\n');

  for (var i; i < data.size(); i++) {
    data[i] = $.trim(data[i]);
    if (data[i])
      result.push(data[i])
  }
}

function fillInData(data) {
  var courseName, courseCode = "";

  for (var i = 0; i < lines.size(); i++) {
    var header = $(lines[i]).find('td.curso')
    if (header.size() > 0) {
      if (courseCode != "") {
        saveCourse({courseCode, courseName, courseSessions});
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
}

getCourses(function(result) {
  lines = $('tr', result);
  fillInData(lines);
});
