import os
import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


# Import your models
# Create and check models
# Run and print your queries
from main_app.models import Student


def add_students():
    Student.objects.create(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date='1995-05-15',
        email='john.doe@university.com'
    )

    student = Student(
        student_id='FE0054',
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@university.com'
    )
    student.save()

    Student.objects.create(
        student_id='FH2014',
        first_name='Alice',
        last_name='Johnson',
        birth_date='1998-02-10',
        email='alice.johnson@university.com'
    )

    Student.objects.create(
        student_id='FH2015',
        first_name='Bob',
        last_name='Wilson',
        birth_date='1996-11-25',
        email='bob.wilson@university.com'
    )


def get_students_info():
    current_info = []
    students_info = Student.objects.all()
    for student in students_info:
        current_info.append(f"Student №{student.student_id}: "
                            f"{student.first_name} {student.last_name}; Email: {student.email}")

    return '\n'.join(current_info)


def update_students_emails():
    students = Student.objects.all()
    for student in students:
        new_email = student.email.replace('university.com', "uni-students.com")
        student.email = new_email
        student.save()


def truncate_students():
    Student.objects.all().delete()


