from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import xml.etree.ElementTree as ET
from .models import Student


@csrf_exempt
def create_student(request):
    if request.method != "POST":
        return HttpResponse(
            "<response><status>error</status><message>Only POST allowed</message></response>",
            content_type="application/xml",
            status=405
        )

    try:
        tree = ET.fromstring(request.body)

        name = tree.find("name").text
        email = tree.find("email").text
        course = tree.find("course").text

        student = Student.objects.create(
            name=name,
            email=email,
            course=course
        )

        return HttpResponse(
            f"""
            <response>
                <status>success</status>
                <id>{student.id}</id>
            </response>
            """,
            content_type="application/xml"
        )

    except Exception as e:
        return HttpResponse(
            f"<response><status>error</status><message>{str(e)}</message></response>",
            content_type="application/xml",
            status=400
        )

def get_students(request):
    if request.method == "GET":
        students = Student.objects.all()

        root = ET.Element("students")

        for s in students:
            student_elem = ET.SubElement(root, "student")
            ET.SubElement(student_elem, "id").text = str(s.id)
            ET.SubElement(student_elem, "name").text = s.name
            ET.SubElement(student_elem, "email").text = s.email
            ET.SubElement(student_elem, "course").text = s.course

        return HttpResponse(
            ET.tostring(root),
            content_type="application/xml"
        )

@csrf_exempt
def update_student(request, id):
    if request.method == "PUT":
        try:
            student = Student.objects.get(id=id)
            tree = ET.fromstring(request.body)

            student.name = tree.find("name").text
            student.email = tree.find("email").text
            student.course = tree.find("course").text
            student.save()

            return HttpResponse(
                "<response><status>updated</status></response>",
                content_type="application/xml"
            )

        except Student.DoesNotExist:
            return HttpResponse(
                "<response><status>error</status><message>Not found</message></response>",
                content_type="application/xml",
                status=404
            )

@csrf_exempt
def delete_student(request, id):
    if request.method == "DELETE":
        try:
            student = Student.objects.get(id=id)
            student.delete()

            return HttpResponse(
                "<response><status>deleted</status></response>",
                content_type="application/xml"
            )

        except Student.DoesNotExist:
            return HttpResponse(
                "<response><status>error</status><message>Not found</message></response>",
                content_type="application/xml",
                status=404
            )