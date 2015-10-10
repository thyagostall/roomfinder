from urllib.request import urlopen
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View

from . import models

import json


class FindFreeRoomAt(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(FindFreeRoomAt, self).dispatch(request, *args, **kwargs)

    def get(self, request, time):
        result = {}

        dataset_schedules = models.Schedule.objects.exclude(time=time)
        for i, available in zip(range(len(dataset_schedules)), dataset_schedules):
            result[i] = {available.room: available.time}

        return HttpResponse(json.dumps(result), content_type="application/json")


class ImportData(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ImportData, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        majors = get_majors()

        result = ""
        for major in majors:
            page = urlopen("https://utfws.utfpr.edu.br/rptacad/" + major)

            table = page.read().decode("iso-8859-1")
            start = table.index("<table border")
            end = table.index("</body>")
            table = table[start:end]

            result += table

        return HttpResponse(result)

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        parse_courses(data)
        return HttpResponse('Data saved successfully!')


def parse_professors(db_session, new_professors):
    db_session.professors.clear()

    for new_professor in new_professors:
        dataset = models.Professor.objects.filter(name=new_professor)

        if dataset:
            db_professor = dataset[0]
        else:
            db_professor = models.Professor(name=new_professor)
            db_professor.save()

        db_session.professors.add(db_professor)


def get_or_insert_room(room_number):
    dataset = models.Room.objects.filter(number=room_number)

    if dataset:
        result = dataset[0]
    else:
        result = models.Room(number=room_number, locked=False)
        result.save()

    return result


def parse_courses(courses):
    for course in courses:
        dataset_course = models.Course.objects.filter(code=course['courseCode'])

        if dataset_course:
            db_course = dataset_course[0]
        else:
            db_course = models.Course(code=course['courseCode'], name=course['courseName'])
            db_course.save()

        sessions = course['courseSessions']
        for session in sessions:
            dataset_sessions = models.Session.objects.filter(code=session['session'], course=db_course)

            if dataset_sessions:
                db_session = dataset_sessions[0]
            else:
                db_session = models.Session(code=session['session'], course=db_course)
                db_session.save()

            if session['professor']:
                parse_professors(db_session, session['professor'])

            schedules = session['schedule']
            if schedules:
                for schedule in schedules:
                    db_room = get_or_insert_room(schedule['room'])
                    dataset_schedules = models.Schedule.objects.filter(session=db_session, time=schedule['time'], room=db_room)

                    if dataset_schedules:
                        db_schedule = dataset_schedules[0]
                    else:
                        db_schedule = models.Schedule(session=db_session, time=schedule['time'], room=db_room)
                        db_schedule.save()


def get_majors():
    return [
        "10B1365A17409CCE0B0DC14DD0A94696.html",
        "AB08BD77DCD4D4E4D836E89250B262B0.html",
        "4BD08CBAD0CF649EE840380FB2334E72.html",
        "99AA296C0D2435C64E67391C68F77EC7.html",
        "EA60074F8ADEC87A981D73478B889C0F.html",
        "4329EF67E3E03E21B25EADEAE019E9B7.html",
        "632CAE37DAD39C0F981BED197A7EE063.html",
        "15D70569D0536FDA730F999312907E45.html",
        "9F6CA24944C0C522D67432EA937889A4.html",
        "D6DB462CFDFBE9C22A46EEFAA115BAF3.html",
        "242FBA24A7DC506FB4A8023E986C0DC9.html",
        "427E13D7328F6CFD957454F82F421ECC.html",
        "D0D754CA8DBCD31C7B72A3E2B9CFC2C3.html",
        "292568D1F7ACA9AF6703556C281F879E.html",
        "1E62E1B543BA2B45AC3F916463481EF5.html",
        "84BDB746AC9065C4EC3F7407C4659F32.html",
        "2EB9586E949AC4ADA612C19B9337C2B8.html",
        "F8105E891B38DD665F9B1633845BB88D.html",
        "5F29C60CAFA8940E2EE980A325164BEF.html",
        "1F5DF0446141C5E97BD887BC4E2E0298.html",
        "5DD63B78B9CE01FE3D2D96822AB5479C.html",
        "A3E14DD90E4BE31704D8F09C1A885251.html",
        "467D6D9F42CFC61F3C478B0E4BB0F861.html",
        "AF28213FF834B0CB5D359F5ED13B6E80.html",
        "22F512F3396BDAA46AC5999A3CDBE787.html",
        "2E37F05B29130E35D795B7A5FBC4C266.html",
        "5F4D4E1D8E56732CA9A3F5A28CFD2AB7.html",
        "C131BC2A9EF9609F980FC2320553ABBA.html",
        "69D0C51CCD183B60808704A64293C7F4.html",
        "ECAF4628B17F24B4072161EE007D80E9.html",
        "4D22713024EBAFEC229114B2EB576607.html",
        "D90DDA5E52578B467612AE56D26845D5.html",
        "E65F63272BB2E987ED4A05FB8BDAD673.html",
        "79AD9B5E1B9D8C0B73C04B800CB87F1E.html",
        "81175A747AF228DAD5F96B25F2CC3566.html",
        "67F141A35D27193661621C51DD76E809.html",
        "35FE5FDF28E8FDCBED0326A5779ADC35.html",
        "4CB12744FC3775921118EAC96A79BBC6.html",
        "D4FD709BA4E59DCF96075F561C17EA87.html",
        "8881B946AC589122D54180E263F07BEC.html",
        "7B32EDEBB910D79CC8AC70F306DE2D3E.html",
        "61F1F51E9417EF39C2507A6C9EC23DD6.html",
        "A5D31660531657326F148259DF7DCFF4.html",
        "607A510C688A7040123133232F3871EE.html",
        "691D229CDD6AE7EFCEFBC9BCB9B7DF10.html",
        "04DB9C52B7274D62548D936E3974B145.html",
        "6B384DDCAC2656AC221224F912DCD8D1.html",
        "4BCA735384846DA335630A521579F0CC.html"]
