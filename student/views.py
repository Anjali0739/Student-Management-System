from django.shortcuts import render, get_object_or_404, redirect
from .models import Parent, Student
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from school.views import create_notification

# Make sure you have this function defined somewhere
# from school.views import create_notification
# or define it here if needed

@login_required
def add_student(request):
    if request.method == "POST":
        # collect data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        joining_date = request.POST.get('joining_date')
        student_class = request.POST.get('student_class')
        section = request.POST.get('section')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        student_image = request.FILES.get('student_image')

        # parent info
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile = request.POST.get('father_mobile')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile = request.POST.get('mother_mobile')
        mother_email = request.POST.get('mother_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        parent = Parent.objects.create(
            father_name=father_name,
            father_occupation=father_occupation,
            father_mobile=father_mobile,
            father_email=father_email,
            mother_name=mother_name,
            mother_occupation=mother_occupation,
            mother_mobile=mother_mobile,
            mother_email=mother_email,
            present_address=present_address,
            permanent_address=permanent_address,
        )

        Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            student_id=student_id,
            gender=gender,
            date_of_birth=date_of_birth,
            joining_date=joining_date,
            student_class=student_class,
            section=section,
            mobile_number=mobile_number,
            admission_number=admission_number,
            student_image=student_image,
            parent=parent,
        )

        return redirect('student_list')

    return render(request, "students/student_form.html")


@login_required
def student_list(request):
    students = Student.objects.select_related('parent').all()
    unread_notifications = request.user.notification_set.filter(is_read=False)
    context = {
        'student_list': students,
        'unread_notifications': unread_notifications
    }
    return render(request, "students/students.html", context)


@login_required
def edit_student(request, slug):
    student = get_object_or_404(Student, student_id=slug)
    parent = student.parent

    if request.method == "POST":
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.student_id = request.POST.get('student_id')
        student.gender = request.POST.get('gender')
        student.date_of_birth = request.POST.get('date_of_birth')
        student.joining_date = request.POST.get('joining_date')
        student.student_class = request.POST.get('student_class')
        student.section = request.POST.get('section')
        student.mobile_number = request.POST.get('mobile_number')
        student.admission_number = request.POST.get('admission_number')

        if request.FILES.get('student_image'):
            student.student_image = request.FILES.get('student_image')

        student.save()

        # update parent info
        parent.father_name = request.POST.get('father_name')
        parent.father_occupation = request.POST.get('father_occupation')
        parent.father_mobile = request.POST.get('father_mobile')
        parent.father_email = request.POST.get('father_email')
        parent.mother_name = request.POST.get('mother_name')
        parent.mother_occupation = request.POST.get('mother_occupation')
        parent.mother_mobile = request.POST.get('mother_mobile')
        parent.mother_email = request.POST.get('mother_email')
        parent.present_address = request.POST.get('present_address')
        parent.permanent_address = request.POST.get('permanent_address')
        parent.save()

        return redirect('student_list')

    return render(request, "students/student_form.html", {"student": student, "parent": parent})



@login_required
def view_student(request, slug):
    student = get_object_or_404(Student, student_id=slug)
    return render(request, "students/student-details.html", {'student': student})


@login_required
def delete_student(request, slug):
    if request.method == 'POST':
        student = get_object_or_404(Student,student_id=slug)
        student_name = f"{student.first_name} {student.last_name}"
        student.delete()

        create_notification(request.user, f"Deleted Student: {student_name}")
        messages.success(request, f"{student_name} deleted successfully!")
        return redirect('student_list')

    return HttpResponseForbidden()
